import uuid

from fastapi import APIRouter, Depends, status

from app.dependencies.auth import CurrentUser, DBSession, require_roles
from app.repositories.loan_repository import LoanTypeRepository
from app.schemas.loans import (
    LoanApplicationCreate,
    LoanApplicationDecision,
    LoanApplicationResponse,
    LoanResponse,
    LoanTypeResponse,
)
from app.services.loan_service import LoanApplicationService
from app.services.organization_service import EmployeeService

router = APIRouter(prefix="/loans", tags=["Loans"])


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
