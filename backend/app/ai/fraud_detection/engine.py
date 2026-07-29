"""
Fraud Detection Engine.

Combines deterministic rule-based checks (duplicate PAN, salary anomaly,
multiple simultaneous applications) with an unsupervised IsolationForest
anomaly score to produce a composite fraud risk score and a list of
triggered alert types with severities.
"""
from dataclasses import dataclass

import numpy as np
from sklearn.ensemble import IsolationForest

from app.core.logging_config import get_logger

logger = get_logger(__name__)

# Trained once at process start on a synthetic baseline of "normal" applicant behavior.
# In production this is retrained nightly (see background_tasks.ai_tasks.retrain_fraud_model)
# on real anonymized transaction/application data.
_RNG = np.random.default_rng(7)


def _bootstrap_isolation_forest() -> IsolationForest:
    n = 5000
    salary = _RNG.lognormal(10.5, 0.35, n)
    requested = salary * _RNG.uniform(0.1, 2.0, n)
    apps_last_30_days = _RNG.poisson(0.4, n)
    salary_volatility = _RNG.uniform(0, 0.15, n)
    doc_forgery_score = _RNG.beta(1, 20, n)  # mostly near 0
    X = np.column_stack([salary, requested, apps_last_30_days, salary_volatility, doc_forgery_score])
    model = IsolationForest(n_estimators=200, contamination=0.03, random_state=42)
    model.fit(X)
    return model


_isolation_forest = _bootstrap_isolation_forest()


@dataclass
class FraudSignals:
    duplicate_pan_count: int
    salary_volatility_pct: float  # stddev/mean of last N payroll cycles
    active_applications_last_30_days: int
    document_forgery_score: float  # 0-1, from OCR/forgery module
    monthly_net_salary: float
    requested_amount: float


def evaluate_fraud_signals(signals: FraudSignals) -> dict:
    alerts = []

    if signals.duplicate_pan_count > 1:
        alerts.append(
            {
                "alert_type": "DUPLICATE_PAN",
                "severity": "CRITICAL",
                "detail": f"PAN matches {signals.duplicate_pan_count} employee records across the platform.",
            }
        )

    if signals.salary_volatility_pct > 0.35:
        alerts.append(
            {
                "alert_type": "SALARY_ANOMALY",
                "severity": "HIGH" if signals.salary_volatility_pct > 0.6 else "MEDIUM",
                "detail": f"Salary volatility of {signals.salary_volatility_pct:.0%} over recent payroll cycles exceeds normal range.",
            }
        )

    if signals.active_applications_last_30_days > 2:
        alerts.append(
            {
                "alert_type": "MULTIPLE_APPLICATIONS",
                "severity": "HIGH",
                "detail": f"{signals.active_applications_last_30_days} active loan applications within 30 days.",
            }
        )

    if signals.document_forgery_score > 0.5:
        alerts.append(
            {
                "alert_type": "DOCUMENT_FORGERY",
                "severity": "CRITICAL" if signals.document_forgery_score > 0.8 else "HIGH",
                "detail": f"Uploaded document forgery score {signals.document_forgery_score:.2f} exceeds acceptable threshold.",
            }
        )

    X = np.array(
        [[
            signals.monthly_net_salary,
            signals.requested_amount,
            signals.active_applications_last_30_days,
            signals.salary_volatility_pct,
            signals.document_forgery_score,
        ]]
    )
    anomaly_raw = _isolation_forest.decision_function(X)[0]  # higher = more normal
    anomaly_risk = float(np.clip(1 - (anomaly_raw + 0.5), 0, 1))  # normalize to ~0-1 risk

    rule_risk = min(1.0, 0.25 * len(alerts) + max((a["severity"] == "CRITICAL" for a in alerts), default=0) * 0.3)
    composite_risk_score = round(min(1.0, 0.6 * rule_risk + 0.4 * anomaly_risk), 4)

    if not alerts and composite_risk_score > 0.55:
        alerts.append(
            {
                "alert_type": "BEHAVIORAL_ANOMALY",
                "severity": "MEDIUM",
                "detail": "Unsupervised model flagged this application as statistically unusual.",
            }
        )

    has_critical_alert = any(a["severity"] == "CRITICAL" for a in alerts)
    is_high_risk = composite_risk_score >= 0.6 or has_critical_alert

    logger.info("fraud_evaluation", risk_score=composite_risk_score, alert_count=len(alerts), is_high_risk=is_high_risk)

    return {
        "risk_score": composite_risk_score,
        "anomaly_score": round(anomaly_risk, 4),
        "alerts": alerts,
        # A single CRITICAL-severity signal (e.g. confirmed duplicate PAN) always routes to
        # high-risk handling even if the blended composite score sits below the numeric
        # threshold - severity classification is a deliberate override, not just an input
        # to the weighted average.
        "is_high_risk": is_high_risk,
    }
