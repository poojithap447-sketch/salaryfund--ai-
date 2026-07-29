"""
Payroll domain: monthly payroll runs synced from employer HRMS / uploaded manually.
"""
import enum
import uuid
from datetime import date

from sqlalchemy import Enum, ForeignKey, Integer, Numeric, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class PayrollStatus(str, enum.Enum):
    PENDING = "PENDING"
    PROCESSED = "PROCESSED"
    FAILED = "FAILED"


class Payroll(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "payrolls"
    __table_args__ = (UniqueConstraint("employee_id", "cycle_month", "cycle_year", name="uq_payroll_employee_cycle"),)

    employee_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("employees.id", ondelete="CASCADE"), index=True)
    employer_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("employers.id", ondelete="CASCADE"), index=True)
    cycle_month: Mapped[int] = mapped_column(Integer, nullable=False)
    cycle_year: Mapped[int] = mapped_column(Integer, nullable=False)
    gross_salary: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    deductions: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    emi_deductions: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    net_salary: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    days_present: Mapped[int | None] = mapped_column(Integer, nullable=True)
    days_absent: Mapped[int | None] = mapped_column(Integer, nullable=True)
    payment_date: Mapped[date | None] = mapped_column(nullable=True)
    status: Mapped[PayrollStatus] = mapped_column(Enum(PayrollStatus, name="payroll_status_enum"), default=PayrollStatus.PENDING)
    source: Mapped[str] = mapped_column(String(32), default="MANUAL_UPLOAD")  # MANUAL_UPLOAD | HRMS_SYNC | API
