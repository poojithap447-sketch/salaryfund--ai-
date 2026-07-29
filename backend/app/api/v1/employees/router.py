import uuid

from fastapi import APIRouter, Depends, Query, status

from app.dependencies.auth import CurrentUser, DBSession, require_roles
from app.schemas.organization import EmployeeCreate, EmployeeResponse, EmployeeUpdate
from app.services.organization_service import EmployeeService

router = APIRouter(prefix="/employees", tags=["Employees"])


@router.post(
    "",
    response_model=EmployeeResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles("EMPLOYER_ADMIN", "PLATFORM_ADMIN"))],
)
async def onboard_employee(payload: EmployeeCreate, db: DBSession):
    """Employer admins onboard employees onto the platform (creates linked user + profile)."""
    service = EmployeeService(db)
    return await service.onboard_employee(payload)


@router.get("/me", response_model=EmployeeResponse)
async def get_my_profile(current_user: CurrentUser, db: DBSession):
    service = EmployeeService(db)
    return await service.get_employee_by_user(current_user)


@router.get("/{employee_id}", response_model=EmployeeResponse)
async def get_employee(employee_id: uuid.UUID, db: DBSession):
    service = EmployeeService(db)
    return await service.get_employee_or_404(employee_id)


@router.patch(
    "/{employee_id}",
    response_model=EmployeeResponse,
    dependencies=[Depends(require_roles("EMPLOYER_ADMIN", "PLATFORM_ADMIN"))],
)
async def update_employee(employee_id: uuid.UUID, payload: EmployeeUpdate, db: DBSession):
    service = EmployeeService(db)
    return await service.update_employee(employee_id, payload)


@router.get(
    "/employer/{employer_id}",
    response_model=list[EmployeeResponse],
    dependencies=[Depends(require_roles("EMPLOYER_ADMIN", "PLATFORM_ADMIN"))],
)
async def list_employer_employees(
    employer_id: uuid.UUID,
    db: DBSession,
    offset: int = Query(0, ge=0),
    limit: int = Query(100, le=500),
):
    service = EmployeeService(db)
    return await service.list_for_employer(employer_id, offset, limit)
