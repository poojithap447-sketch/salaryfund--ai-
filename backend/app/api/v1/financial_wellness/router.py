from fastapi import APIRouter

from app.dependencies.auth import CurrentUser, DBSession
from app.schemas.ai_and_wellness import FinancialWellnessResponse
from app.services.financial_wellness_service import FinancialWellnessService
from app.services.organization_service import EmployeeService

router = APIRouter(prefix="/financial-wellness", tags=["Financial Wellness"])


@router.get("/me", response_model=FinancialWellnessResponse)
async def get_my_wellness(current_user: CurrentUser, db: DBSession):
    employee_service = EmployeeService(db)
    employee = await employee_service.get_employee_by_user(current_user)
    service = FinancialWellnessService(db)
    return await service.get_latest(employee.id)


@router.post("/me/recompute", response_model=FinancialWellnessResponse)
async def recompute_my_wellness(current_user: CurrentUser, db: DBSession):
    employee_service = EmployeeService(db)
    employee = await employee_service.get_employee_by_user(current_user)
    service = FinancialWellnessService(db)
    return await service.compute_and_store(employee.id)
