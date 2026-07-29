import uuid
from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.models.ai_and_wellness import FraudAlertSeverity, FraudAlertStatus, NotificationChannel, NotificationStatus


class CareerScoreResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    employee_id: uuid.UUID
    score: int
    band: str
    employment_stability_score: Decimal
    salary_growth_score: Decimal
    attendance_score: Decimal
    promotion_score: Decimal
    performance_score: Decimal
    repayment_behavior_score: Decimal
    computed_at: datetime


class CareerScoreHistoryItem(BaseModel):
    score: int
    band: str
    computed_at: datetime


class FinancialWellnessResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    employee_id: uuid.UUID
    debt_to_income_ratio: Decimal
    savings_ratio: Decimal
    emi_burden_ratio: Decimal
    loan_utilization_ratio: Decimal
    emergency_reserve_months: Decimal
    wellness_score: Decimal
    wellness_band: str
    recommendations: dict | None
    computed_at: datetime


class FraudAlertResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    employee_id: uuid.UUID | None
    loan_application_id: uuid.UUID | None
    alert_type: str
    severity: FraudAlertSeverity
    risk_score: Decimal
    status: FraudAlertStatus
    details: dict | None
    created_at: datetime


class FraudAlertResolve(BaseModel):
    status: FraudAlertStatus
    resolution_notes: str | None = None


class NotificationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    channel: NotificationChannel
    template_code: str
    title: str
    body: str
    status: NotificationStatus
    sent_at: datetime | None
    read_at: datetime | None
    created_at: datetime


class PayrollUploadRow(BaseModel):
    employee_code: str
    cycle_month: int
    cycle_year: int
    gross_salary: Decimal
    deductions: Decimal = Decimal("0")
    days_present: int | None = None
    days_absent: int | None = None
    payment_date: date | None = None


class PayrollResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    employee_id: uuid.UUID
    cycle_month: int
    cycle_year: int
    gross_salary: Decimal
    net_salary: Decimal
    emi_deductions: Decimal
    status: str
