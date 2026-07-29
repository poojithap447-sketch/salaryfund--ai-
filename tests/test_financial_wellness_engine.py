"""Unit tests for the Financial Wellness calculation engine (pure function, no DB)."""
from app.ai.financial_wellness.engine import WellnessInputs, calculate_financial_wellness


def test_healthy_profile_gets_good_band():
    inputs = WellnessInputs(
        monthly_net_salary=60000, total_monthly_debt_payments=6000, monthly_savings=12000,
        total_active_loan_principal=20000, total_sanctioned_loan_limit=300000,
        liquid_savings_balance=180000, monthly_essential_expenses=30000,
    )
    result = calculate_financial_wellness(inputs)
    assert result["wellness_score"] > 60
    assert result["wellness_band"] in ("GOOD", "EXCELLENT")
    assert result["recommendations"]["tips"]


def test_at_risk_profile_flags_high_debt_burden():
    inputs = WellnessInputs(
        monthly_net_salary=30000, total_monthly_debt_payments=18000, monthly_savings=500,
        total_active_loan_principal=250000, total_sanctioned_loan_limit=280000,
        liquid_savings_balance=5000, monthly_essential_expenses=25000,
    )
    result = calculate_financial_wellness(inputs)
    assert result["wellness_score"] < 50
    assert any("debt" in tip.lower() or "emi" in tip.lower() for tip in result["recommendations"]["tips"])


def test_ratios_computed_correctly():
    inputs = WellnessInputs(
        monthly_net_salary=50000, total_monthly_debt_payments=10000, monthly_savings=5000,
        total_active_loan_principal=100000, total_sanctioned_loan_limit=200000,
        liquid_savings_balance=50000, monthly_essential_expenses=25000,
    )
    result = calculate_financial_wellness(inputs)
    assert result["debt_to_income_ratio"] == 0.2
    assert result["loan_utilization_ratio"] == 0.5
    assert result["emergency_reserve_months"] == 2.0
