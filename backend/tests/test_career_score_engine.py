"""Unit tests for the Career Credit Score calculation engine (pure function, no DB)."""
from app.ai.career_credit.engine import CareerScoreInputs, calculate_career_score


def test_score_within_bounds():
    inputs = CareerScoreInputs(
        tenure_months=36, number_of_employers_last_5_years=1, salary_growth_pct_yoy=8,
        attendance_pct=95, promotions_count=1, tenure_years_total=3, performance_rating=4.0,
        on_time_emi_payments=10, total_emi_payments=10, num_defaults=0,
    )
    result = calculate_career_score(inputs)
    assert 300 <= result["score"] <= 900
    assert result["band"] in ("EXCELLENT", "GOOD", "FAIR", "POOR")


def test_strong_profile_scores_higher_than_weak_profile():
    strong = CareerScoreInputs(
        tenure_months=60, number_of_employers_last_5_years=1, salary_growth_pct_yoy=15,
        attendance_pct=98, promotions_count=2, tenure_years_total=5, performance_rating=4.8,
        on_time_emi_payments=20, total_emi_payments=20, num_defaults=0,
    )
    weak = CareerScoreInputs(
        tenure_months=4, number_of_employers_last_5_years=4, salary_growth_pct_yoy=-5,
        attendance_pct=60, promotions_count=0, tenure_years_total=0.3, performance_rating=1.5,
        on_time_emi_payments=2, total_emi_payments=10, num_defaults=3,
    )
    strong_result = calculate_career_score(strong)
    weak_result = calculate_career_score(weak)
    assert strong_result["score"] > weak_result["score"]


def test_first_time_borrower_gets_neutral_repayment_score():
    inputs = CareerScoreInputs(
        tenure_months=12, number_of_employers_last_5_years=1, salary_growth_pct_yoy=5,
        attendance_pct=90, promotions_count=0, tenure_years_total=1, performance_rating=3.5,
        on_time_emi_payments=0, total_emi_payments=0, num_defaults=0,
    )
    result = calculate_career_score(inputs)
    assert result["repayment_behavior_score"] == 65.0
