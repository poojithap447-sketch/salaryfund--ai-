"""
Organization domain: Employer, Department, Employee.
"""
import enum
import uuid
from datetime import date

from sqlalchemy import Boolean, Date, Enum, ForeignKey, Numeric, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class EmployerStatus(str, enum.Enum):
    PENDING_VERIFICATION = "PENDING_VERIFICATION"
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    TERMINATED = "TERMINATED"


class Employer(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "employers"

    admin_user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    legal_name: Mapped[str] = mapped_column(String(255), nullable=False)
    trade_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    registration_number: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    gstin: Mapped[str | None] = mapped_column(String(20), nullable=True)
    industry: Mapped[str | None] = mapped_column(String(128), nullable=True)
    employee_count_band: Mapped[str | None] = mapped_column(String(32), nullable=True)
    status: Mapped[EmployerStatus] = mapped_column(Enum(EmployerStatus, name="employer_status_enum"), default=EmployerStatus.PENDING_VERIFICATION)
    payroll_cycle_day: Mapped[int] = mapped_column(default=1, nullable=False)  # day of month payroll runs
    max_salary_advance_pct: Mapped[float] = mapped_column(Numeric(5, 2), default=50.00)  # % of salary employees may draw
    address: Mapped[str | None] = mapped_column(String(500), nullable=True)
    city: Mapped[str | None] = mapped_column(String(100), nullable=True)
    state: Mapped[str | None] = mapped_column(String(100), nullable=True)
    country: Mapped[str] = mapped_column(String(100), default="India")

    admin_user: Mapped["User"] = relationship(back_populates="employer_profile")  # noqa: F821
    departments: Mapped[list["Department"]] = relationship(back_populates="employer", cascade="all, delete-orphan")
    employees: Mapped[list["Employee"]] = relationship(back_populates="employer")


class Department(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "departments"
    __table_args__ = (UniqueConstraint("employer_id", "name", name="uq_department_employer_name"),)

    employer_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("employers.id", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    cost_center_code: Mapped[str | None] = mapped_column(String(32), nullable=True)

    employer: Mapped["Employer"] = relationship(back_populates="departments")
    employees: Mapped[list["Employee"]] = relationship(back_populates="department")


class EmploymentStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    ON_LEAVE = "ON_LEAVE"
    SUSPENDED = "SUSPENDED"
    RESIGNED = "RESIGNED"
    TERMINATED = "TERMINATED"


class Employee(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "employees"
    __table_args__ = (UniqueConstraint("employer_id", "employee_code", name="uq_employee_employer_code"),)

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    employer_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("employers.id", ondelete="CASCADE"), index=True)
    department_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("departments.id", ondelete="SET NULL"), nullable=True)

    employee_code: Mapped[str] = mapped_column(String(64), nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    designation: Mapped[str | None] = mapped_column(String(128), nullable=True)
    date_of_joining: Mapped[date] = mapped_column(Date, nullable=False)
    date_of_birth: Mapped[date | None] = mapped_column(Date, nullable=True)
    employment_status: Mapped[EmploymentStatus] = mapped_column(
        Enum(EmploymentStatus, name="employment_status_enum"), default=EmploymentStatus.ACTIVE
    )

    # PII - stored encrypted at the application layer (see app/utils/encryption.py)
    pan_encrypted: Mapped[str | None] = mapped_column(String(512), nullable=True)
    aadhaar_encrypted: Mapped[str | None] = mapped_column(String(512), nullable=True)
    bank_account_encrypted: Mapped[str | None] = mapped_column(String(512), nullable=True)
    ifsc_code: Mapped[str | None] = mapped_column(String(16), nullable=True)

    monthly_gross_salary: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    monthly_net_salary: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)

    is_kyc_verified: Mapped[bool] = mapped_column(Boolean, default=False)

    employer: Mapped["Employer"] = relationship(back_populates="employees")
    department: Mapped["Department"] = relationship(back_populates="employees")
    user: Mapped["User"] = relationship(back_populates="employee_profile")  # noqa: F821
