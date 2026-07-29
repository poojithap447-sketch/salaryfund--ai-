import uuid

from fastapi import APIRouter, Depends, status

from app.dependencies.auth import DBSession, require_roles
from app.schemas.organization import DepartmentCreate, DepartmentResponse, EmployerCreate, EmployerResponse
from app.services.organization_service import EmployerService

router = APIRouter(prefix="/employers", tags=["Employers"])


@router.post(
    "",
    response_model=EmployerResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles("PLATFORM_ADMIN"))],
)
async def onboard_employer(payload: EmployerCreate, db: DBSession):
    """Platform admins onboard new employer organizations onto SalaryFund AI."""
    service = EmployerService(db)
    return await service.onboard_employer(payload)


@router.get(
    "/{employer_id}",
    response_model=EmployerResponse,
    dependencies=[Depends(require_roles("PLATFORM_ADMIN", "EMPLOYER_ADMIN"))],
)
async def get_employer(employer_id: uuid.UUID, db: DBSession):
    service = EmployerService(db)
    return await service.get_employer_or_404(employer_id)


@router.post(
    "/{employer_id}/departments",
    response_model=DepartmentResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles("EMPLOYER_ADMIN", "PLATFORM_ADMIN"))],
)
async def create_department(employer_id: uuid.UUID, payload: DepartmentCreate, db: DBSession):
    service = EmployerService(db)
    return await service.create_department(employer_id, payload)


@router.get(
    "/{employer_id}/departments",
    response_model=list[DepartmentResponse],
    dependencies=[Depends(require_roles("EMPLOYER_ADMIN", "PLATFORM_ADMIN"))],
)
async def list_departments(employer_id: uuid.UUID, db: DBSession):
    service = EmployerService(db)
    return await service.list_departments(employer_id)
