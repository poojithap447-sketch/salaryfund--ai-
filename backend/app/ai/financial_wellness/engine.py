"""
Financial Wellness Engine.

Computes standard personal-finance health ratios and derives a 0-100 wellness
score plus actionable, plain-language recommendations.
"""
from dataclasses import dataclass


@dataclass
class WellnessInputs:
    monthly_net_salary: float
    total_monthly_debt_payments: float  # all EMIs across lenders
    monthly_savings: float
    total_active_loan_principal: float
    total_sanctioned_loan_limit: float
    liquid_savings_balance: float
    monthly_essential_expenses: float


def calculate_financial_wellness(i: WellnessInputs) -> dict:
    salary = max(i.monthly_net_salary, 1e-6)

    debt_to_income_ratio = round(i.total_monthly_debt_payments / salary, 4)
    savings_ratio = round(i.monthly_savings / salary, 4)
    emi_burden_ratio = round(i.total_monthly_debt_payments / salary, 4)
    loan_utilization_ratio = round(
        i.total_active_loan_principal / max(i.total_sanctioned_loan_limit, 1e-6), 4
    ) if i.total_sanctioned_loan_limit > 0 else 0.0
    emergency_reserve_months = round(
        i.liquid_savings_balance / max(i.monthly_essential_expenses, 1e-6), 2
    )

    # Sub-scores (0-100), higher is healthier
    dti_score = max(0, 100 - debt_to_income_ratio * 150)
    savings_score = min(100, savings_ratio * 400)
    emi_burden_score = max(0, 100 - emi_burden_ratio * 160)
    utilization_score = max(0, 100 - loan_utilization_ratio * 100)
    reserve_score = min(100, emergency_reserve_months / 6 * 100)  # 6 months = full marks

    wellness_score = round(
        0.25 * dti_score + 0.20 * savings_score + 0.20 * emi_burden_score + 0.15 * utilization_score + 0.20 * reserve_score,
        2,
    )
    wellness_score = max(0.0, min(100.0, wellness_score))

    if wellness_score >= 80:
        band = "EXCELLENT"
    elif wellness_score >= 60:
        band = "GOOD"
    elif wellness_score >= 40:
        band = "NEEDS_ATTENTION"
    else:
        band = "AT_RISK"

    recommendations = _build_recommendations(
        debt_to_income_ratio, savings_ratio, emi_burden_ratio, loan_utilization_ratio, emergency_reserve_months
    )

    return {
        "debt_to_income_ratio": debt_to_income_ratio,
        "savings_ratio": savings_ratio,
        "emi_burden_ratio": emi_burden_ratio,
        "loan_utilization_ratio": loan_utilization_ratio,
        "emergency_reserve_months": emergency_reserve_months,
        "wellness_score": wellness_score,
        "wellness_band": band,
        "recommendations": recommendations,
    }


def _build_recommendations(dti, savings_ratio, emi_burden, utilization, reserve_months) -> dict:
    tips = []
    if dti > 0.45:
        tips.append("Your debt-to-income ratio is high. Consider consolidating loans or pausing new borrowing.")
    if savings_ratio < 0.10:
        tips.append("Aim to save at least 10% of your net salary each month via an auto-debit savings plan.")
    if emi_burden > 0.40:
        tips.append("EMI payments exceed 40% of your salary. Explore restructuring or a longer tenure to reduce monthly burden.")
    if utilization > 0.75:
        tips.append("You are utilizing most of your sanctioned loan limit. Avoid taking on additional credit right now.")
    if reserve_months < 3:
        tips.append("Build an emergency fund covering at least 3 months of essential expenses.")
    if not tips:
        tips.append("Your financial health looks strong. Keep maintaining consistent savings and timely repayments.")
    return {"tips": tips, "priority_action": tips[0]}
