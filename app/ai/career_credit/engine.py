"""
Career Credit Score(tm) Engine.

Produces a 300-900 score (mirroring familiar credit-bureau scales) from six
weighted sub-scores derived from employment and repayment behavior data.
Each sub-score is normalized 0-100 before weighting.
"""
from dataclasses import dataclass

WEIGHTS = {
    "employment_stability": 0.20,
    "salary_growth": 0.15,
    "attendance": 0.15,
    "promotion": 0.15,
    "performance": 0.15,
    "repayment_behavior": 0.20,
}

SCORE_MIN, SCORE_MAX = 300, 900


@dataclass
class CareerScoreInputs:
    tenure_months: float
    number_of_employers_last_5_years: int
    salary_growth_pct_yoy: float
    attendance_pct: float  # 0-100
    promotions_count: int
    tenure_years_total: float
    performance_rating: float  # 0-5 scale from employer HRMS
    on_time_emi_payments: int
    total_emi_payments: int
    num_defaults: int


def _employment_stability_score(i: CareerScoreInputs) -> float:
    tenure_component = min(100, (i.tenure_months / 60) * 100)  # 5 years tenure => full marks
    hopping_penalty = max(0, (i.number_of_employers_last_5_years - 1) * 12)
    return max(0.0, min(100.0, tenure_component - hopping_penalty))


def _salary_growth_score(i: CareerScoreInputs) -> float:
    # 0% growth -> 40 pts, 10% -> 75 pts, 20%+ -> 100 pts; negative growth penalized
    if i.salary_growth_pct_yoy <= 0:
        return max(0.0, 40 + i.salary_growth_pct_yoy * 2)
    return min(100.0, 40 + i.salary_growth_pct_yoy * 3)


def _attendance_score(i: CareerScoreInputs) -> float:
    return max(0.0, min(100.0, i.attendance_pct))


def _promotion_score(i: CareerScoreInputs) -> float:
    if i.tenure_years_total <= 0:
        return 50.0
    promotion_rate = i.promotions_count / max(i.tenure_years_total, 1)
    return max(0.0, min(100.0, promotion_rate * 60 + 30))


def _performance_score(i: CareerScoreInputs) -> float:
    return max(0.0, min(100.0, (i.performance_rating / 5.0) * 100))


def _repayment_behavior_score(i: CareerScoreInputs) -> float:
    if i.total_emi_payments == 0:
        return 65.0  # neutral prior for first-time borrowers
    on_time_ratio = i.on_time_emi_payments / i.total_emi_payments
    default_penalty = min(60, i.num_defaults * 20)
    return max(0.0, min(100.0, on_time_ratio * 100 - default_penalty))


def calculate_career_score(inputs: CareerScoreInputs) -> dict:
    sub_scores = {
        "employment_stability_score": round(_employment_stability_score(inputs), 2),
        "salary_growth_score": round(_salary_growth_score(inputs), 2),
        "attendance_score": round(_attendance_score(inputs), 2),
        "promotion_score": round(_promotion_score(inputs), 2),
        "performance_score": round(_performance_score(inputs), 2),
        "repayment_behavior_score": round(_repayment_behavior_score(inputs), 2),
    }

    weighted_pct = (
        sub_scores["employment_stability_score"] * WEIGHTS["employment_stability"]
        + sub_scores["salary_growth_score"] * WEIGHTS["salary_growth"]
        + sub_scores["attendance_score"] * WEIGHTS["attendance"]
        + sub_scores["promotion_score"] * WEIGHTS["promotion"]
        + sub_scores["performance_score"] * WEIGHTS["performance"]
        + sub_scores["repayment_behavior_score"] * WEIGHTS["repayment_behavior"]
    ) / 100.0

    score = round(SCORE_MIN + weighted_pct * (SCORE_MAX - SCORE_MIN))
    score = max(SCORE_MIN, min(SCORE_MAX, score))

    if score >= 780:
        band = "EXCELLENT"
    elif score >= 650:
        band = "GOOD"
    elif score >= 500:
        band = "FAIR"
    else:
        band = "POOR"

    return {"score": score, "band": band, **sub_scores, "feature_breakdown": {"weights": WEIGHTS, "inputs": inputs.__dict__}}
