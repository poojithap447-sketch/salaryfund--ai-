"""
Generates a realistic synthetic dataset to bootstrap the eligibility models before
enough real repayment history exists. Once the platform has accumulated real
loan-outcome data (see app.repositories.loan_repository), the training pipeline
(app/ai/training/train_eligibility.py) should be pointed at the real data extract
instead - this module exists purely to make the platform trainable/demoable on day one.
"""
import numpy as np
import pandas as pd

from app.ai.eligibility.features import FEATURE_NAMES

RNG = np.random.default_rng(42)


def generate_dataset(n_samples: int = 8000) -> pd.DataFrame:
    monthly_net_salary = RNG.lognormal(mean=10.5, sigma=0.4, size=n_samples)  # ~ INR 30k - 150k
    requested_amount = monthly_net_salary * RNG.uniform(0.2, 3.0, size=n_samples)
    requested_tenure_months = RNG.integers(3, 36, size=n_samples).astype(float)
    tenure_at_employer_months = RNG.integers(1, 180, size=n_samples).astype(float)
    career_credit_score = RNG.normal(650, 110, size=n_samples).clip(300, 900)
    existing_active_loans = RNG.integers(0, 4, size=n_samples).astype(float)
    debt_to_income_ratio = RNG.uniform(0, 0.9, size=n_samples)
    emi_burden_ratio = RNG.uniform(0, 0.7, size=n_samples)
    attendance_score = RNG.uniform(50, 100, size=n_samples)
    avg_repayment_delay_days = RNG.exponential(scale=3, size=n_samples)
    salary_growth_pct_yoy = RNG.normal(6, 8, size=n_samples)
    num_previous_defaults = RNG.poisson(0.15, size=n_samples).astype(float)
    age_years = RNG.integers(21, 58, size=n_samples).astype(float)

    salary_to_request_ratio = monthly_net_salary / np.maximum(requested_amount, 1)

    df = pd.DataFrame(
        {
            "monthly_net_salary": monthly_net_salary,
            "requested_amount": requested_amount,
            "requested_tenure_months": requested_tenure_months,
            "salary_to_request_ratio": salary_to_request_ratio,
            "tenure_at_employer_months": tenure_at_employer_months,
            "career_credit_score": career_credit_score,
            "existing_active_loans": existing_active_loans,
            "debt_to_income_ratio": debt_to_income_ratio,
            "emi_burden_ratio": emi_burden_ratio,
            "attendance_score": attendance_score,
            "avg_repayment_delay_days": avg_repayment_delay_days,
            "salary_growth_pct_yoy": salary_growth_pct_yoy,
            "num_previous_defaults": num_previous_defaults,
            "age_years": age_years,
        }
    )
    df = df[FEATURE_NAMES]

    # Ground-truth generative rule (logit combination of risk factors) + noise,
    # mirrors real-world underwriting heuristics used to bootstrap supervised training.
    logit = (
        3.2
        + 0.006 * (career_credit_score - 650)
        - 3.0 * debt_to_income_ratio
        - 2.2 * emi_burden_ratio
        + 0.015 * tenure_at_employer_months.clip(max=60)
        - 0.9 * existing_active_loans
        - 1.4 * num_previous_defaults
        - 0.05 * avg_repayment_delay_days
        + 0.02 * salary_growth_pct_yoy
        + 1.1 * (salary_to_request_ratio.clip(max=3) - 1)
        + RNG.normal(0, 0.6, size=n_samples)
    )
    prob_approve = 1 / (1 + np.exp(-logit))
    df["approved"] = (RNG.uniform(size=n_samples) < prob_approve).astype(int)
    return df
