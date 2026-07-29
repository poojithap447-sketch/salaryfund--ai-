"""Unit tests for the Fraud Detection engine (pure function, no DB)."""
from app.ai.fraud_detection.engine import FraudSignals, evaluate_fraud_signals


def test_duplicate_pan_triggers_critical_alert():
    signals = FraudSignals(
        duplicate_pan_count=3, salary_volatility_pct=0.05, active_applications_last_30_days=1,
        document_forgery_score=0.1, monthly_net_salary=50000, requested_amount=20000,
    )
    result = evaluate_fraud_signals(signals)
    alert_types = [a["alert_type"] for a in result["alerts"]]
    assert "DUPLICATE_PAN" in alert_types
    assert result["is_high_risk"] is True


def test_clean_application_has_low_risk():
    signals = FraudSignals(
        duplicate_pan_count=1, salary_volatility_pct=0.03, active_applications_last_30_days=0,
        document_forgery_score=0.05, monthly_net_salary=60000, requested_amount=15000,
    )
    result = evaluate_fraud_signals(signals)
    assert result["risk_score"] < 0.6


def test_document_forgery_triggers_alert():
    signals = FraudSignals(
        duplicate_pan_count=1, salary_volatility_pct=0.02, active_applications_last_30_days=0,
        document_forgery_score=0.85, monthly_net_salary=50000, requested_amount=10000,
    )
    result = evaluate_fraud_signals(signals)
    alert_types = [a["alert_type"] for a in result["alerts"]]
    assert "DOCUMENT_FORGERY" in alert_types
