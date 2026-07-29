"""Unit tests for the Fraud Detection engine (app.ai.fraud_detection.engine)."""
from app.ai.fraud_detection.engine import FraudSignals, evaluate_fraud_signals


def test_clean_application_is_low_risk():
    result = evaluate_fraud_signals(
        FraudSignals(
            duplicate_pan_count=1, salary_volatility_pct=0.05, active_applications_last_30_days=0,
            document_forgery_score=0.02, monthly_net_salary=45000, requested_amount=20000,
        )
    )
    assert result["is_high_risk"] is False
    assert result["risk_score"] < 0.6


def test_duplicate_pan_triggers_critical_alert():
    result = evaluate_fraud_signals(
        FraudSignals(
            duplicate_pan_count=3, salary_volatility_pct=0.05, active_applications_last_30_days=0,
            document_forgery_score=0.02, monthly_net_salary=45000, requested_amount=20000,
        )
    )
    alert_types = [a["alert_type"] for a in result["alerts"]]
    assert "DUPLICATE_PAN" in alert_types
    assert any(a["severity"] == "CRITICAL" for a in result["alerts"])


def test_multiple_signals_compound_risk_score():
    result = evaluate_fraud_signals(
        FraudSignals(
            duplicate_pan_count=2, salary_volatility_pct=0.5, active_applications_last_30_days=4,
            document_forgery_score=0.85, monthly_net_salary=45000, requested_amount=90000,
        )
    )
    assert result["is_high_risk"] is True
    assert len(result["alerts"]) >= 3
