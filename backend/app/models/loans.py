"""
Loan domain: Lender, LoanType, LoanPolicy, InterestRate, LoanApplication, Loan, EMI, Transaction.
"""
import enum
import uuid
from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, Enum, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class Lender(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "lenders"

    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    license_number: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    contact_email: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    max_exposure_limit: Mapped[float] = mapped_column(Numeric(16, 2), default=0)
    api_webhook_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    interest_rates: Mapped[list["InterestRate"]] = relationship(back_populates="lender", cascade="all, delete-orphan")
    loans: Mapped[list["Loan"]] = relationship(back_populates="lender")


class LoanTypeCode(str, enum.Enum):
    SALARY_ADVANCE = "SALARY_ADVANCE"
    PERSONAL_LOAN = "PERSONAL_LOAN"
    EMERGENCY_LOAN = "EMERGENCY_LOAN"
    EDUCATION_LOAN = "EDUCATION_LOAN"
    MEDICAL_LOAN = "MEDICAL_LOAN"


class LoanType(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "loan_types"

    code: Mapped[LoanTypeCode] = mapped_column(Enum(LoanTypeCode, name="loan_type_code_enum"), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    min_amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    max_amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    min_tenure_months: Mapped[int] = mapped_column(Integer, nullable=False)
    max_tenure_months: Mapped[int] = mapped_column(Integer, nullable=False)
    requires_collateral: Mapped[bool] = mapped_column(Boolean, default=False)

    policies: Mapped[list["LoanPolicy"]] = relationship(back_populates="loan_type", cascade="all, delete-orphan")


class LoanPolicy(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Business rules engine config per loan type - drives eligibility pre-checks."""
    __tablename__ = "loan_policies"

    loan_type_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("loan_types.id", ondelete="CASCADE"), index=True)
    min_tenure_months_employed: Mapped[int] = mapped_column(Integer, default=3)
    min_career_credit_score: Mapped[int] = mapped_column(Integer, default=500)
    max_dti_ratio: Mapped[float] = mapped_column(Numeric(5, 2), default=45.00)
    max_active_loans: Mapped[int] = mapped_column(Integer, default=2)
    max_pct_of_monthly_salary: Mapped[float] = mapped_column(Numeric(5, 2), default=50.00)
    cooling_period_days: Mapped[int] = mapped_column(Integer, default=30)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    loan_type: Mapped["LoanType"] = relationship(back_populates="policies")


class InterestRate(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "interest_rates"

    lender_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("lenders.id", ondelete="CASCADE"), index=True)
    loan_type_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("loan_types.id", ondelete="CASCADE"), index=True)
    risk_band: Mapped[str] = mapped_column(String(16), nullable=False)  # e.g. "A", "B", "C", "D"
    annual_rate_pct: Mapped[float] = mapped_column(Numeric(6, 3), nullable=False)
    processing_fee_pct: Mapped[float] = mapped_column(Numeric(5, 2), default=1.00)
    effective_from: Mapped[date] = mapped_column(Date, nullable=False)
    effective_to: Mapped[date | None] = mapped_column(Date, nullable=True)

    lender: Mapped["Lender"] = relationship(back_populates="interest_rates")


class LoanApplicationStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    SUBMITTED = "SUBMITTED"
    UNDER_AI_REVIEW = "UNDER_AI_REVIEW"
    UNDER_MANUAL_REVIEW = "UNDER_MANUAL_REVIEW"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    WITHDRAWN = "WITHDRAWN"
    FLAGGED_FRAUD = "FLAGGED_FRAUD"


class LoanApplication(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "loan_applications"

    employee_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("employees.id", ondelete="CASCADE"), index=True)
    loan_type_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("loan_types.id"), index=True)
    requested_amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    requested_tenure_months: Mapped[int] = mapped_column(Integer, nullable=False)
    purpose: Mapped[str | None] = mapped_column(String(500), nullable=True)
    status: Mapped[LoanApplicationStatus] = mapped_column(
        Enum(LoanApplicationStatus, name="loan_application_status_enum"), default=LoanApplicationStatus.DRAFT
    )
    submitted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    decisioned_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    rejection_reason: Mapped[str | None] = mapped_column(String(500), nullable=True)
    reviewed_by_user_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)

    employee: Mapped["Employee"] = relationship()  # noqa: F821
    loan_type: Mapped["LoanType"] = relationship()
    ai_prediction: Mapped["AIPrediction"] = relationship(back_populates="loan_application", uselist=False)
    loan: Mapped["Loan"] = relationship(back_populates="application", uselist=False)


class LoanStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    CLOSED = "CLOSED"
    DEFAULTED = "DEFAULTED"
    WRITTEN_OFF = "WRITTEN_OFF"
    RESTRUCTURED = "RESTRUCTURED"


class Loan(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "loans"

    application_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("loan_applications.id", ondelete="CASCADE"), unique=True)
    employee_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("employees.id"), index=True)
    lender_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("lenders.id"), index=True)
    principal_amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    interest_rate_pct: Mapped[float] = mapped_column(Numeric(6, 3), nullable=False)
    tenure_months: Mapped[int] = mapped_column(Integer, nullable=False)
    processing_fee: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    disbursed_amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    disbursed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[LoanStatus] = mapped_column(Enum(LoanStatus, name="loan_status_enum"), default=LoanStatus.ACTIVE)
    outstanding_principal: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    closed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    application: Mapped["LoanApplication"] = relationship(back_populates="loan")
    lender: Mapped["Lender"] = relationship(back_populates="loans")
    emis: Mapped[list["EMI"]] = relationship(back_populates="loan", cascade="all, delete-orphan", order_by="EMI.installment_number")


class EMIStatus(str, enum.Enum):
    UPCOMING = "UPCOMING"
    DUE = "DUE"
    PAID = "PAID"
    OVERDUE = "OVERDUE"
    PARTIALLY_PAID = "PARTIALLY_PAID"
    WAIVED = "WAIVED"


class EMI(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "emis"

    loan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("loans.id", ondelete="CASCADE"), index=True)
    installment_number: Mapped[int] = mapped_column(Integer, nullable=False)
    due_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    principal_component: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    interest_component: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    emi_amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    amount_paid: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    status: Mapped[EMIStatus] = mapped_column(Enum(EMIStatus, name="emi_status_enum"), default=EMIStatus.UPCOMING)
    paid_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    late_fee: Mapped[float] = mapped_column(Numeric(12, 2), default=0)

    loan: Mapped["Loan"] = relationship(back_populates="emis")


class TransactionType(str, enum.Enum):
    DISBURSEMENT = "DISBURSEMENT"
    EMI_PAYMENT = "EMI_PAYMENT"
    LATE_FEE = "LATE_FEE"
    REFUND = "REFUND"
    PROCESSING_FEE = "PROCESSING_FEE"
    PAYROLL_DEDUCTION = "PAYROLL_DEDUCTION"


class TransactionStatus(str, enum.Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    REVERSED = "REVERSED"


class Transaction(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "transactions"

    employee_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("employees.id"), index=True)
    loan_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("loans.id"), nullable=True, index=True)
    emi_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("emis.id"), nullable=True)
    transaction_type: Mapped[TransactionType] = mapped_column(Enum(TransactionType, name="transaction_type_enum"), nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    status: Mapped[TransactionStatus] = mapped_column(Enum(TransactionStatus, name="transaction_status_enum"), default=TransactionStatus.PENDING)
    reference_id: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    payment_gateway_ref: Mapped[str | None] = mapped_column(String(128), nullable=True)
    meta: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
