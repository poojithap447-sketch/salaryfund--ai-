"""
Feature engineering for the Loan Eligibility Engine.
Converts raw employee / application / financial-history data into the
fixed-order numeric feature vector consumed by all three candidate models.
"""
from dataclasses import dataclass, fields

import numpy as np
import pandas as pd

FEATURE_NAMES = [
    "monthly_net_salary",
    "requested_amount",
    "requested_tenure_months",
    "salary_to_request_ratio",
    "tenure_at_employer_months",
    "career_credit_score",
    "existing_active_loans",
    "debt_to_income_ratio",
    "emi_burden_ratio",
    "attendance_score",
    "avg_repayment_delay_days",
    "salary_growth_pct_yoy",
    "num_previous_defaults",
    "age_years",
]


@dataclass
class EligibilityFeatures:
    monthly_net_salary: float
    requested_amount: float
    requested_tenure_months: float
    salary_to_request_ratio: float
    tenure_at_employer_months: float
    career_credit_score: float
    existing_active_loans: float
    debt_to_income_ratio: float
    emi_burden_ratio: float
    attendance_score: float
    avg_repayment_delay_days: float
    salary_growth_pct_yoy: float
    num_previous_defaults: float
    age_years: float

    def to_array(self) -> np.ndarray:
        return np.array([getattr(self, f.name) for f in fields(self)], dtype=float).reshape(1, -1)

    def to_dict(self) -> dict:
        return {f.name: getattr(self, f.name) for f in fields(self)}


def build_feature_frame(records: list[dict]) -> pd.DataFrame:
    """Build a pandas DataFrame with a fixed column order for training/inference."""
    df = pd.DataFrame(records)
    for col in FEATURE_NAMES:
        if col not in df.columns:
            df[col] = 0.0
    return df[FEATURE_NAMES]
