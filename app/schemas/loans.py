import uuid
from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.models.loans import EMIStatus, LoanApplicationStatus, LoanStatus, LoanTypeCode


class LoanTypeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    code: LoanTypeCode
    name: str
    description: str | None
    min_amount: Decimal
    max_amount: Decimal
    min_tenure_months: int
    max_tenure_months: int


class LoanApplicationCreate(BaseModel):
    loan_type_id: uuid.UUID
    requested_amount: Decimal = Field(..., gt=0)
    requested_tenure_months: int = Field(..., gt=0)
    purpose: str | None = Field(None, max_length=500)


class LoanApplicationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    employee_id: uuid.UUID
    loan_type_id: uuid.UUID
    requested_amount: Decimal
    requested_tenure_months: int
    purpose: str | None
    status: LoanApplicationStatus
    submitted_at: datetime | None
    decisioned_at: datetime | None
    rejection_reason: str | None
    created_at: datetime


class LoanApplicationDecision(BaseModel):
    approve: bool
    approved_amount: Decimal | None = None
    lender_id: uuid.UUID | None = None
    rejection_reason: str | None = None


class EligibilityCheckResponse(BaseModel):
    """Response of the AI eligibility engine returned inline during application review."""
    model_config = ConfigDict(protected_namespaces=())

    approval_probability: float
    risk_score: float
    eligible_amount: Decimal
    confidence: float
    best_model: str
    model_comparison: dict
    shap_explanation: dict
    decision_hint: str  # "AUTO_APPROVE" | "MANUAL_REVIEW" | "AUTO_REJECT"


class LoanResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    application_id: uuid.UUID
    employee_id: uuid.UUID
    lender_id: uuid.UUID
    principal_amount: Decimal
    interest_rate_pct: Decimal
    tenure_months: int
    disbursed_amount: Decimal
    disbursed_at: datetime | None
    status: LoanStatus
    outstanding_principal: Decimal


class EMIResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    loan_id: uuid.UUID
    installment_number: int
    due_date: date
    principal_component: Decimal
    interest_component: Decimal
    emi_amount: Decimal
    amount_paid: Decimal
    status: EMIStatus
    late_fee: Decimal


class EMIPaymentRequest(BaseModel):
    emi_id: uuid.UUID
    amount: Decimal = Field(..., gt=0)
    payment_gateway_ref: str | None = None
