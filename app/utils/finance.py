"""
Financial calculation utilities: EMI schedule generation using the standard
reducing-balance amortization formula.
"""
from datetime import date
from decimal import ROUND_HALF_UP, Decimal
from dateutil.relativedelta import relativedelta


def calculate_emi_amount(principal: Decimal, annual_rate_pct: Decimal, tenure_months: int) -> Decimal:
    """Standard EMI formula: P * r * (1+r)^n / ((1+r)^n - 1)"""
    principal = Decimal(principal)
    monthly_rate = Decimal(annual_rate_pct) / Decimal(100) / Decimal(12)

    if monthly_rate == 0:
        return (principal / tenure_months).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    factor = (1 + monthly_rate) ** tenure_months
    emi = principal * monthly_rate * factor / (factor - 1)
    return Decimal(emi).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def generate_amortization_schedule(
    principal: Decimal, annual_rate_pct: Decimal, tenure_months: int, first_due_date: date
) -> list[dict]:
    """Returns a list of installment dicts: {installment_number, due_date, principal_component,
    interest_component, emi_amount}."""
    principal = Decimal(principal)
    monthly_rate = Decimal(annual_rate_pct) / Decimal(100) / Decimal(12)
    emi_amount = calculate_emi_amount(principal, annual_rate_pct, tenure_months)

    schedule = []
    outstanding = principal
    due_date = first_due_date

    for month in range(1, tenure_months + 1):
        interest_component = (outstanding * monthly_rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        principal_component = emi_amount - interest_component

        # Final installment absorbs rounding residue so outstanding hits exactly zero.
        if month == tenure_months:
            principal_component = outstanding
            emi_this_month = principal_component + interest_component
        else:
            emi_this_month = emi_amount

        outstanding = outstanding - principal_component

        schedule.append(
            {
                "installment_number": month,
                "due_date": due_date,
                "principal_component": principal_component.quantize(Decimal("0.01")),
                "interest_component": interest_component.quantize(Decimal("0.01")),
                "emi_amount": emi_this_month.quantize(Decimal("0.01")),
            }
        )
        due_date = due_date + relativedelta(months=1)

    return schedule
