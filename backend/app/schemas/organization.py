import uuid
from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.organization import EmployerStatus, EmploymentStatus


class DepartmentCreate(BaseModel):
    name: str = Field(..., max_length=128)
    cost_center_code: str | None = None


class DepartmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    employer_id: uuid.UUID
    name: str
    cost_center_code: str | None


class EmployerCreate(BaseModel):
    legal_name: str = Field(..., max_length=255)
    trade_name: str | None = None
    registration_number: str = Field(..., max_length=64)
    gstin: str | None = None
    industry: str | None = None
    employee_count_band: str | None = None
    admin_email: EmailStr
    admin_phone_number: str
    admin_password: str = Field(..., min_length=8)
    address: str | None = None
    city: str | None = None
    state: str | None = None


class EmployerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    legal_name: str
    trade_name: str | None
    registration_number: str
    status: EmployerStatus
    payroll_cycle_day: int
    max_salary_advance_pct: Decimal
    created_at: datetime


class EmployeeCreate(BaseModel):
    employer_id: uuid.UUID
    department_id: uuid.UUID | None = None
    employee_code: str
    full_name: str
    email: EmailStr
    phone_number: str
    password: str = Field(..., min_length=8)
    designation: str | None = None
    date_of_joining: date
    date_of_birth: date | None = None
    monthly_gross_salary: Decimal
    monthly_net_salary: Decimal
    pan_number: str | None = Field(None, description="Plain PAN - will be encrypted at rest")
    aadhaar_number: str | None = Field(None, description="Plain Aadhaar - will be encrypted at rest")
    bank_account_number: str | None = None
    ifsc_code: str | None = None


class EmployeeUpdate(BaseModel):
    department_id: uuid.UUID | None = None
    designation: str | None = None
    monthly_gross_salary: Decimal | None = None
    monthly_net_salary: Decimal | None = None
    employment_status: EmploymentStatus | None = None


class EmployeeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    employer_id: uuid.UUID
    department_id: uuid.UUID | None
    employee_code: str
    full_name: str
    designation: str | None
    date_of_joining: date
    employment_status: EmploymentStatus
    monthly_gross_salary: Decimal
    monthly_net_salary: Decimal
    is_kyc_verified: bool
    created_at: datetime
