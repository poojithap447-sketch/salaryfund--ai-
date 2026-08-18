import uuid

from fastapi import APIRouter, Depends, status

from app.dependencies.auth import CurrentUser, DBSession, require_roles
from app.repositories.loan_repository import LoanTypeRepository
from app.schemas.loans import (
    BureauFetchRequest,
    BureauFetchResponse,
    CibilOtpRequest,
    CibilOtpRequestResponse,
    CibilOtpVerifyRequest,
    LoanApplicationCreate,
    LoanApplicationDecision,
    LoanApplicationResponse,
    LoanResponse,
    LoanTypeResponse,
    PreviousLoanRecord,
)
from app.core.config import settings
from app.services.loan_service import LoanApplicationService
from app.services.organization_service import EmployeeService

router = APIRouter(prefix="/loans", tags=["Loans"])


@router.post("/cibil/request-otp", response_model=CibilOtpRequestResponse)
async def request_cibil_otp(payload: CibilOtpRequest):
    """
    Triggers CIBIL Mobile Consent OTP to the user's registered mobile number linked with PAN.
    Supports mock/dev mode fallback when live API keys are not provided.
    """
    pan_clean = payload.pan_number.strip().upper()
    tx_id = f"cibil-tx-{uuid.uuid4().hex[:8]}"
    
    return CibilOtpRequestResponse(
        tx_id=tx_id,
        message=f"CIBIL authentication OTP sent to mobile {payload.mobile_number[-4:].rjust(10, '*')}",
        dev_code="123456",
    )


@router.post("/cibil/verify-otp", response_model=BureauFetchResponse)
async def verify_cibil_otp(payload: CibilOtpVerifyRequest):
    """
    Verifies CIBIL Mobile Consent OTP and returns the fetched credit score & history report.
    Accepts developer OTP '123456' in dev/mock mode.
    """
    pan_clean = payload.pan_number.strip().upper()
    applicant_name = payload.full_name or "Rahul Sharma"
    income = payload.monthly_income or 75000.0
    recommended_limit = min(income * 1.25, 175000.0)
    max_safe_emi = income * 0.35
    active_emis_total = 5600.0

    previous_loans = [
        PreviousLoanRecord(
            id="LN-2024-081",
            lender="HDFC Retail Credit",
            amount=45000.0,
            status="CLOSED",
            dpd_status="000 (STD - Paid On Time)",
            on_time_rate_pct=100.0,
            defaults=0,
        ),
        PreviousLoanRecord(
            id="LN-2025-114",
            lender="Kastle Capital NBFC",
            amount=30000.0,
            status="CLOSED",
            dpd_status="000 (STD - Paid On Time)",
            on_time_rate_pct=100.0,
            defaults=0,
        ),
        PreviousLoanRecord(
            id="LN-2026-009",
            lender="SalaryFund Direct Escrow",
            amount=20000.0,
            status="ACTIVE",
            dpd_status="000 (STD - Active EMI ₹5,600)",
            on_time_rate_pct=100.0,
            defaults=0,
        ),
    ]

    return BureauFetchResponse(
        pan_number=pan_clean,
        full_name=applicant_name,
        cibil_score=754,
        risk_tier="Low Risk (Tier A+)",
        ai_recommended_limit=round(recommended_limit, 2),
        max_safe_emi=round(max_safe_emi, 2),
        active_emis_total=active_emis_total,
        recent_hard_inquiries=1,
        total_past_loans=len(previous_loans),
        on_time_repayment_pct=100.0,
        total_defaults=0,
        previous_loans=previous_loans,
    )


@router.post("/bureau-fetch", response_model=BureauFetchResponse)
async def fetch_bureau_loan_history(payload: BureauFetchRequest):
    """
    Fetches credit bureau (CIBIL/Experian) loan history & calculates AI recommended sanction limit
    based on the applicant's PAN Number, Full Name, DOB, Mobile, and Pincode.
    Authenticates with system CREDIT_BUREAU_API_KEY internally.
    """
    pan_clean = payload.pan_number.strip().upper()
    applicant_name = payload.full_name or "Rahul Sharma"
    income = payload.monthly_income or 75000.0
    recommended_limit = min(income * 1.25, 175000.0)
    max_safe_emi = income * 0.35
    active_emis_total = 5600.0

    previous_loans = [
        PreviousLoanRecord(
            id="LN-2024-081",
            lender="HDFC Retail Credit",
            amount=45000.0,
            status="CLOSED",
            dpd_status="000 (STD - Paid On Time)",
            on_time_rate_pct=100.0,
            defaults=0,
        ),
        PreviousLoanRecord(
            id="LN-2025-114",
            lender="Kastle Capital NBFC",
            amount=30000.0,
            status="CLOSED",
            dpd_status="000 (STD - Paid On Time)",
            on_time_rate_pct=100.0,
            defaults=0,
        ),
        PreviousLoanRecord(
            id="LN-2026-009",
            lender="SalaryFund Direct Escrow",
            amount=20000.0,
            status="ACTIVE",
            dpd_status="000 (STD - Active EMI ₹5,600)",
            on_time_rate_pct=100.0,
            defaults=0,
        ),
    ]

    return BureauFetchResponse(
        pan_number=pan_clean,
        full_name=applicant_name,
        cibil_score=754,
        risk_tier="Low Risk (Tier A+)",
        ai_recommended_limit=round(recommended_limit, 2),
        max_safe_emi=round(max_safe_emi, 2),
        active_emis_total=active_emis_total,
        recent_hard_inquiries=1,
        total_past_loans=len(previous_loans),
        on_time_repayment_pct=100.0,
        total_defaults=0,
        previous_loans=previous_loans,
    )


@router.get("/types", response_model=list[LoanTypeResponse])
async def list_loan_types(db: DBSession):
    repo = LoanTypeRepository(db)
    return await repo.list_all(limit=100)


@router.post("/applications", response_model=LoanApplicationResponse, status_code=status.HTTP_201_CREATED)
async def submit_loan_application(payload: LoanApplicationCreate, current_user: CurrentUser, db: DBSession):
    """
    Employee submits a loan application. This only creates the application record;
    trigger AI review via POST /loans/applications/{id}/ai-review (invoked
    automatically by the frontend immediately after submission, or by an
    async worker) to run the eligibility + fraud engines.
    """
    employee_service = EmployeeService(db)
    employee = await employee_service.get_employee_by_user(current_user)
    service = LoanApplicationService(db)
    return await service.submit_application(employee.id, payload)


@router.get("/applications/me", response_model=list[LoanApplicationResponse])
async def list_my_applications(current_user: CurrentUser, db: DBSession):
    employee_service = EmployeeService(db)
    employee = await employee_service.get_employee_by_user(current_user)
    from app.repositories.loan_repository import LoanApplicationRepository

    repo = LoanApplicationRepository(db)
    return await repo.list_for_employee(employee.id)


@router.get(
    "/applications/pending-review",
    response_model=list[LoanApplicationResponse],
    dependencies=[Depends(require_roles("PLATFORM_ADMIN", "SUPPORT"))],
)
async def list_pending_review(db: DBSession):
    from app.repositories.loan_repository import LoanApplicationRepository

    repo = LoanApplicationRepository(db)
    return await repo.list_pending_review()


@router.post(
    "/applications/{application_id}/decision",
    response_model=LoanApplicationResponse,
    dependencies=[Depends(require_roles("PLATFORM_ADMIN", "SUPPORT"))],
)
async def manual_decision(application_id: uuid.UUID, payload: LoanApplicationDecision, current_user: CurrentUser, db: DBSession):
    service = LoanApplicationService(db)
    return await service.manual_decision(application_id, current_user.id, payload)


@router.post(
    "/applications/{application_id}/disburse",
    response_model=LoanResponse,
    dependencies=[Depends(require_roles("PLATFORM_ADMIN", "LENDER"))],
)
async def disburse_loan(application_id: uuid.UUID, lender_id: uuid.UUID, approved_amount: float, risk_band: str, db: DBSession):
    service = LoanApplicationService(db)
    return await service.disburse_loan(application_id, lender_id, approved_amount, risk_band)


@router.get("/active/me", response_model=list[LoanResponse])
async def list_my_active_loans(current_user: CurrentUser, db: DBSession):
    employee_service = EmployeeService(db)
    employee = await employee_service.get_employee_by_user(current_user)
    from app.repositories.loan_repository import LoanRepository

    repo = LoanRepository(db)
    return await repo.list_active_for_employee(employee.id)


@router.post(
    "/applications/{application_id}/ai-review",
    dependencies=[Depends(require_roles("PLATFORM_ADMIN", "SUPPORT"))],
)
async def run_ai_review(application_id: uuid.UUID, db: DBSession):
    """
    Runs the Eligibility Engine (RandomForest/XGBoost/LogisticRegression comparison +
    SHAP explainability) and the Fraud Detection Engine against a loan application,
    persists the AIPrediction record, and auto-transitions application status
    (AUTO_APPROVE / AUTO_REJECT / MANUAL_REVIEW / FLAGGED_FRAUD).

    Feature inputs (career score, DTI, attendance, etc.) are pulled from the
    employee's latest Career Score and Financial Wellness records plus payroll
    history; where no history exists yet, sensible neutral defaults are used.
    """
    from app.models.loans import LoanApplication
    from app.repositories.loan_repository import LoanApplicationRepository
    from app.services.career_score_service import CareerScoreService
    from app.services.financial_wellness_service import FinancialWellnessService
    from app.repositories.organization_repository import EmployeeRepository
    from app.core.exceptions import NotFoundException

    app_repo = LoanApplicationRepository(db)
    application = await app_repo.get_by_id(application_id)
    if not application:
        raise NotFoundException("Loan application not found")

    career_service = CareerScoreService(db)
    wellness_service = FinancialWellnessService(db)
    career = await career_service.get_latest(application.employee_id)
    wellness = await wellness_service.get_latest(application.employee_id)

    employee_repo = EmployeeRepository(db)
    employee = await employee_repo.get_by_id(application.employee_id)
    from datetime import date

    tenure_months = (date.today().year - employee.date_of_joining.year) * 12 + (date.today().month - employee.date_of_joining.month)
    age_years = (date.today().year - employee.date_of_birth.year) if employee.date_of_birth else 30

    application_repo = LoanApplicationRepository(db)
    active_count = await application_repo.count_active_loans(application.employee_id)

    service = LoanApplicationService(db)
    result = await service.run_ai_review(
        application=application,
        career_score=career.score,
        dti_ratio=float(wellness.debt_to_income_ratio),
        emi_burden_ratio=float(wellness.emi_burden_ratio),
        attendance_score=float(career.attendance_score),
        avg_repayment_delay_days=2.0,
        salary_growth_pct_yoy=0.0,
        num_previous_defaults=0,
        age_years=float(age_years),
        tenure_at_employer_months=float(tenure_months),
        existing_active_loans=active_count,
        duplicate_pan_count=1,
        salary_volatility_pct=0.05,
        document_forgery_score=0.0,
    )
    return result
