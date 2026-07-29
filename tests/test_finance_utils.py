"""Unit tests for EMI amortization math - pure functions, no DB needed."""
from datetime import date
from decimal import Decimal

from app.utils.finance import calculate_emi_amount, generate_amortization_schedule


def test_calculate_emi_amount_standard():
    emi = calculate_emi_amount(Decimal("100000"), Decimal("12"), 12)
    # Known correct EMI for 100000 @ 12% p.a. over 12 months ~= 8884.88
    assert abs(float(emi) - 8884.88) < 1.0


def test_calculate_emi_zero_interest():
    emi = calculate_emi_amount(Decimal("12000"), Decimal("0"), 12)
    assert emi == Decimal("1000.00")


def test_amortization_schedule_sums_to_principal():
    schedule = generate_amortization_schedule(Decimal("50000"), Decimal("14"), 6, date(2026, 1, 1))
    assert len(schedule) == 6
    total_principal = sum(row["principal_component"] for row in schedule)
    assert abs(float(total_principal) - 50000.0) < 0.5


def test_amortization_schedule_due_dates_increment_monthly():
    schedule = generate_amortization_schedule(Decimal("10000"), Decimal("10"), 3, date(2026, 3, 15))
    assert schedule[0]["due_date"] == date(2026, 3, 15)
    assert schedule[1]["due_date"] == date(2026, 4, 15)
    assert schedule[2]["due_date"] == date(2026, 5, 15)


def test_interest_component_decreases_over_time():
    schedule = generate_amortization_schedule(Decimal("100000"), Decimal("12"), 12, date(2026, 1, 1))
    assert schedule[0]["interest_component"] > schedule[-1]["interest_component"]
    assert schedule[0]["principal_component"] < schedule[-1]["principal_component"]
