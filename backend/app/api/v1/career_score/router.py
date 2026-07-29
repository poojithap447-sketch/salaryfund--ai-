import uuid

from fastapi import APIRouter

from app.dependencies.auth import CurrentUser, DBSession
from app.schemas.ai_and_wellness import CareerScoreResponse
from app.services.career_score_service import CareerScoreService
from app.services.organization_service import EmployeeService

router = APIRouter(prefix="/career-score", tags=["Career Credit Score"])


@router.get("/me", response_model=CareerScoreResponse)
async def get_my_score(current_user: CurrentUser, db: DBSession):
    employee_service = EmployeeService(db)
    employee = await employee_service.get_employee_by_user(current_user)
    service = CareerScoreService(db)
    return await service.get_latest(employee.id)


@router.post("/me/recompute", response_model=CareerScoreResponse)
async def recompute_my_score(current_user: CurrentUser, db: DBSession):
    employee_service = EmployeeService(db)
    employee = await employee_service.get_employee_by_user(current_user)
    service = CareerScoreService(db)
    return await service.compute_and_store(employee.id)


@router.get("/me/history")
async def get_my_score_history(current_user: CurrentUser, db: DBSession):
    employee_service = EmployeeService(db)
    employee = await employee_service.get_employee_by_user(current_user)
    service = CareerScoreService(db)
    history = await service.get_history(employee.id)
    return [{"score": h.score, "band": h.band, "computed_at": h.computed_at} for h in history]


@router.get("/{employee_id}", response_model=CareerScoreResponse)
async def get_employee_score(employee_id: uuid.UUID, db: DBSession):
    service = CareerScoreService(db)
    return await service.get_latest(employee_id)
