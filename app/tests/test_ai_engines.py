"""
Unit tests for the AI engines: Eligibility (RF/XGBoost/LogisticRegression +
SHAP), Fraud Detection, Career Credit Score, and Financial Wellness. These
run the actual trained artifacts / actual sklearn models - no mocking - since
the whole point of this suite is to catch regressions in the math/pipelines.
"""
import pytest

from app.ai.career_credit.engine import CareerScoreInputs, calculate_career_score
from app.ai.eligibility.engine import EligibilityEngine
from app.ai.eligibility.features import EligibilityFeatures
from app.ai.financial_wellness.engine import WellnessInputs, calculate_financial_wellness
from app.ai.fraud_detection.engine import FraudSignals, evaluate_fraud_signals


def _sample_features(**overrides) -> EligibilityFeatures:
    base = dict(
        monthly_net_salary=60000, requested_amount=50000, requested_tenure_months=6,
        salary_to_request_ratio=1.2, tenure_at_employer_months=24, career_credit_score=700,
        existing_active_loans=0, debt_to_income_ratio=0.2, emi_burden_ratio=0.15,
        attendance_score=95, avg_repayment_delay_days=1, salary_growth_pct_yoy=8,
        num_previous_defaults=0, age_years=32,
    )
    base.update(overrides)
    return EligibilityFeatures(**base)


def test_eligibility_engine_returns_all_three_model_probabilities():
    result = EligibilityEngine.instance().predict(_sample_features())
    probs = result["model_comparison"]["candidate_probabilities"]
    assert set(probs.keys()) == {"random_forest", "xgboost", "logistic_regression"}
    for p in probs.values():
        assert 0.0 <= p <= 1.0
    assert result["decision_hint"] in ("AUTO_APPROVE", "AUTO_REJECT", "MANUAL_REVIEW")
    assert 0.0 <= result["confidence"] <= 1.0


def test_eligibility_engine_shap_explanation_present():
    result = EligibilityEngine.instance().predict(_sample_features())
    shap = result["shap_explanation"]
    assert "feature_contributions" in shap
    assert len(shap["feature_contributions"]) > 0


def test_eligibility_high_risk_profile_scores_lower_than_strong_profile():
    strong = EligibilityEngine.instance().predict(_sample_features())
    weak = EligibilityEngine.instance().predict(
        _sample_features(
            career_credit_score=350,
            debt_to_income_ratio=0.85,
            emi_burden_ratio=0.6,
            existing_active_loans=3,
            num_previous_defaults=3,
        )
    )
    assert weak["approval_probability"] < strong["approval_probability"]


def test_fraud_engine_flags_duplicate_pan():
    result = evaluate_fraud_signals(FraudSignals(2, 0.05, 0, 0.0, 50000, 20000))
    alert_types = [a["alert_type"] for a in result["alerts"]]
    assert "DUPLICATE_PAN" in alert_types
    assert result["is_high_risk"] is True


def test_fraud_engine_clean_profile_not_flagged():
    result = evaluate_fraud_signals(FraudSignals(1, 0.05, 0, 0.0, 50000, 20000))
    assert result["risk_score"] < 0.6


def test_career_score_within_bounds():
    result = calculate_career_score(
        CareerScoreInputs(
            tenure_months=36, number_of_employers_last_5_years=1, salary_growth_pct_yoy=8,
            attendance_pct=92, promotions_count=1, tenure_years_total=3, performance_rating=4.2,
            on_time_emi_payments=10, total_emi_payments=10, num_defaults=0,
        )
    )
    assert 300 <= result["score"] <= 900
    assert result["band"] in ("EXCELLENT", "GOOD", "FAIR", "POOR")


def test_career_score_penalizes_defaults():
    good = calculate_career_score(
        CareerScoreInputs(36, 1, 8, 92, 1, 3, 4.2, 10, 10, 0)
    )
    bad = calculate_career_score(
        CareerScoreInputs(36, 1, 8, 92, 1, 3, 4.2, 3, 10, 4)
    )
    assert bad["score"] < good["score"]


def test_financial_wellness_within_bounds():
    result = calculate_financial_wellness(
        WellnessInputs(
            monthly_net_salary=60000, total_monthly_debt_payments=15000, monthly_savings=5000,
            total_active_loan_principal=100000, total_sanctioned_loan_limit=300000,
            liquid_savings_balance=20000, monthly_essential_expenses=35000,
        )
    )
    assert 0 <= result["wellness_score"] <= 100
    assert result["wellness_band"] in ("EXCELLENT", "GOOD", "NEEDS_ATTENTION", "AT_RISK")
    assert "tips" in result["recommendations"]
