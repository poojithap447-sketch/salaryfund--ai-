import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.organization import Department, Employee, Employer
from app.repositories.base import BaseRepository


class EmployerRepository(BaseRepository[Employer]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Employer)

    async def get_by_registration_number(self, reg_number: str) -> Employer | None:
        result = await self.db.execute(select(Employer).where(Employer.registration_number == reg_number))
        return result.scalar_one_or_none()

    async def get_by_admin_user_id(self, user_id: uuid.UUID) -> Employer | None:
        result = await self.db.execute(select(Employer).where(Employer.admin_user_id == user_id))
        return result.scalar_one_or_none()


class DepartmentRepository(BaseRepository[Department]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Department)

    async def list_for_employer(self, employer_id: uuid.UUID):
        result = await self.db.execute(select(Department).where(Department.employer_id == employer_id))
        return result.scalars().all()


class EmployeeRepository(BaseRepository[Employee]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Employee)

    async def get_by_user_id(self, user_id: uuid.UUID) -> Employee | None:
        result = await self.db.execute(select(Employee).where(Employee.user_id == user_id))
        return result.scalar_one_or_none()

    async def get_by_employee_code(self, employer_id: uuid.UUID, employee_code: str) -> Employee | None:
        result = await self.db.execute(
            select(Employee).where(Employee.employer_id == employer_id, Employee.employee_code == employee_code)
        )
        return result.scalar_one_or_none()

    async def get_by_code_any_employer(self, employee_code: str) -> Employee | None:
        result = await self.db.execute(
            select(Employee).where(func.lower(Employee.employee_code) == employee_code.lower())
        )
        return result.scalars().first()


    async def list_for_employer(self, employer_id: uuid.UUID, offset: int = 0, limit: int = 100):
        result = await self.db.execute(
            select(Employee).where(Employee.employer_id == employer_id).offset(offset).limit(limit)
        )
        return result.scalars().all()

    async def count_by_pan_hash(self, pan_encrypted_candidates: list[str]) -> int:
        """Used by fraud detection to spot duplicate-PAN across different employee records."""
        if not pan_encrypted_candidates:
            return 0
        result = await self.db.execute(
            select(func.count()).select_from(Employee).where(Employee.pan_encrypted.in_(pan_encrypted_candidates))
        )
        return result.scalar_one()
