import uuid

from fastapi import APIRouter, Depends

from app.dependencies.auth import CurrentUser, DBSession, require_roles
from app.schemas.ai_and_wellness import PayrollResponse, PayrollUploadRow
from app.services.organization_service import EmployeeService
from app.services.payroll_service import PayrollService

router = APIRouter(prefix="/payroll", tags=["Payroll"])


@router.post(
    "/employer/{employer_id}/upload",
    response_model=list[PayrollResponse],
    dependencies=[Depends(require_roles("EMPLOYER_ADMIN", "PLATFORM_ADMIN"))],
)
async def upload_payroll(employer_id: uuid.UUID, rows: list[PayrollUploadRow], db: DBSession):
    """Bulk-ingests a payroll cycle (CSV parsed client-side or via the frontend upload form)."""
    service = PayrollService(db)
    return await service.bulk_ingest(employer_id, rows)


@router.get("/me", response_model=list[PayrollResponse])
async def my_payroll_history(current_user: CurrentUser, db: DBSession):
    employee_service = EmployeeService(db)
    employee = await employee_service.get_employee_by_user(current_user)
    service = PayrollService(db)
    return await service.list_for_employee(employee.id)
