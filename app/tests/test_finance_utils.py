"""
Unit tests for EMI amortization math - verifies the reducing-balance formula
produces a schedule that fully retires principal with the last installment.
"""
from decimal import Decimal

from datetime import date

from app.utils.finance import calculate_emi_amount, generate_amortization_schedule


def test_emi_amount_positive_rate():
    emi = calculate_emi_amount(Decimal("100000"), Decimal("12"), 12)
    assert emi > Decimal("8000")
    assert emi < Decimal("9500")


def test_emi_amount_zero_rate_is_simple_division():
    emi = calculate_emi_amount(Decimal("120000"), Decimal("0"), 12)
    assert emi == Decimal("10000.00")


def test_amortization_schedule_fully_retires_principal():
    schedule = generate_amortization_schedule(Decimal("50000"), Decimal("15"), 6, date(2026, 1, 1))
    assert len(schedule) == 6
    total_principal_paid = sum(row["principal_component"] for row in schedule)
    assert abs(total_principal_paid - Decimal("50000")) < Decimal("0.05")


def test_amortization_schedule_interest_decreases_over_time():
    schedule = generate_amortization_schedule(Decimal("100000"), Decimal("18"), 12, date(2026, 1, 1))
    interest_components = [row["interest_component"] for row in schedule]
    assert interest_components[0] > interest_components[-1]
