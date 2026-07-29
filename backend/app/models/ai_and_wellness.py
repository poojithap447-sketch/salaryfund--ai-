"""
Career Credit Score, Financial Wellness, AI Predictions, Fraud Alerts,
Notifications and Reports.
"""
import enum
import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class CareerCreditScore(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Point-in-time snapshot of an employee's Career Credit Score (300-900)."""
    __tablename__ = "career_credit_scores"

    employee_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("employees.id", ondelete="CASCADE"), index=True)
    score: Mapped[int] = mapped_column(Integer, nullable=False)  # 300-900
    employment_stability_score: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    salary_growth_score: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    attendance_score: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    promotion_score: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    performance_score: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    repayment_behavior_score: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    band: Mapped[str] = mapped_column(String(16), nullable=False)  # EXCELLENT/GOOD/FAIR/POOR
    computed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default="now()")
    feature_breakdown: Mapped[dict | None] = mapped_column(JSONB, nullable=True)


class FinancialWellnessRecord(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "financial_wellness_records"

    employee_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("employees.id", ondelete="CASCADE"), index=True)
    debt_to_income_ratio: Mapped[float] = mapped_column(Numeric(6, 3), nullable=False)
    savings_ratio: Mapped[float] = mapped_column(Numeric(6, 3), nullable=False)
    emi_burden_ratio: Mapped[float] = mapped_column(Numeric(6, 3), nullable=False)
    loan_utilization_ratio: Mapped[float] = mapped_column(Numeric(6, 3), nullable=False)
    emergency_reserve_months: Mapped[float] = mapped_column(Numeric(6, 3), nullable=False)
    wellness_score: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)  # 0-100
    wellness_band: Mapped[str] = mapped_column(String(16), nullable=False)
    recommendations: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    computed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default="now()")


class PredictionType(str, enum.Enum):
    ELIGIBILITY = "ELIGIBILITY"
    FRAUD = "FRAUD"
    CAREER_SCORE = "CAREER_SCORE"
    WELLNESS = "WELLNESS"


class AIPrediction(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Stores every AI inference for auditability / model-monitoring / SHAP explanations."""
    __tablename__ = "ai_predictions"

    loan_application_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("loan_applications.id", ondelete="CASCADE"), nullable=True, unique=True
    )
    employee_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("employees.id"), index=True)
    prediction_type: Mapped[PredictionType] = mapped_column(Enum(PredictionType, name="prediction_type_enum"), nullable=False)
    model_name: Mapped[str] = mapped_column(String(64), nullable=False)  # random_forest | xgboost | logistic_regression | ensemble
    model_version: Mapped[str] = mapped_column(String(32), nullable=False)
    approval_probability: Mapped[float | None] = mapped_column(Numeric(6, 4), nullable=True)
    risk_score: Mapped[float | None] = mapped_column(Numeric(6, 4), nullable=True)
    eligible_amount: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)
    confidence: Mapped[float | None] = mapped_column(Numeric(6, 4), nullable=True)
    shap_values: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    model_comparison: Mapped[dict | None] = mapped_column(JSONB, nullable=True)  # per-model metrics for the comparison
    raw_features: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    inference_latency_ms: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)

    loan_application: Mapped["LoanApplication"] = relationship(back_populates="ai_prediction")  # noqa: F821


class FraudAlertSeverity(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class FraudAlertStatus(str, enum.Enum):
    OPEN = "OPEN"
    UNDER_INVESTIGATION = "UNDER_INVESTIGATION"
    CONFIRMED = "CONFIRMED"
    DISMISSED = "DISMISSED"


class FraudAlert(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "fraud_alerts"

    employee_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("employees.id"), nullable=True, index=True)
    loan_application_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("loan_applications.id"), nullable=True)
    alert_type: Mapped[str] = mapped_column(String(64), nullable=False)  # DUPLICATE_PAN | SALARY_ANOMALY | DOC_FORGERY | MULTI_APPLICATION
    severity: Mapped[FraudAlertSeverity] = mapped_column(Enum(FraudAlertSeverity, name="fraud_alert_severity_enum"), nullable=False)
    risk_score: Mapped[float] = mapped_column(Numeric(6, 4), nullable=False)
    status: Mapped[FraudAlertStatus] = mapped_column(Enum(FraudAlertStatus, name="fraud_alert_status_enum"), default=FraudAlertStatus.OPEN)
    details: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    resolved_by_user_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    resolution_notes: Mapped[str | None] = mapped_column(Text, nullable=True)


class NotificationChannel(str, enum.Enum):
    EMAIL = "EMAIL"
    SMS = "SMS"
    PUSH = "PUSH"
    IN_APP = "IN_APP"


class NotificationStatus(str, enum.Enum):
    PENDING = "PENDING"
    SENT = "SENT"
    FAILED = "FAILED"
    READ = "READ"


class Notification(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "notifications"

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True)
    channel: Mapped[NotificationChannel] = mapped_column(Enum(NotificationChannel, name="notification_channel_enum"), nullable=False)
    template_code: Mapped[str] = mapped_column(String(64), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[NotificationStatus] = mapped_column(Enum(NotificationStatus, name="notification_status_enum"), default=NotificationStatus.PENDING)
    sent_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    read_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    meta: Mapped[dict | None] = mapped_column(JSONB, nullable=True)


class ReportType(str, enum.Enum):
    MONTHLY_PORTFOLIO = "MONTHLY_PORTFOLIO"
    EMPLOYER_UTILIZATION = "EMPLOYER_UTILIZATION"
    FRAUD_SUMMARY = "FRAUD_SUMMARY"
    NPA_REPORT = "NPA_REPORT"
    COLLECTIONS = "COLLECTIONS"


class ReportStatus(str, enum.Enum):
    QUEUED = "QUEUED"
    GENERATING = "GENERATING"
    READY = "READY"
    FAILED = "FAILED"


class Report(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "reports"

    report_type: Mapped[ReportType] = mapped_column(Enum(ReportType, name="report_type_enum"), nullable=False)
    requested_by_user_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    employer_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("employers.id"), nullable=True)
    period_start: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    period_end: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[ReportStatus] = mapped_column(Enum(ReportStatus, name="report_status_enum"), default=ReportStatus.QUEUED)
    file_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    error_message: Mapped[str | None] = mapped_column(String(500), nullable=True)
