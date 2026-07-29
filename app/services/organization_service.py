import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AlreadyExistsException, NotFoundException
from app.models.organization import Employee, Employer
from app.models.rbac import User, UserType
from app.repositories.organization_repository import DepartmentRepository, EmployeeRepository, EmployerRepository
from app.repositories.user_repository import UserRepository
from app.schemas.organization import DepartmentCreate, EmployeeCreate, EmployeeUpdate, EmployerCreate
from app.security.password import hash_password
from app.utils.encryption import encrypt_field


class EmployerService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.employer_repo = EmployerRepository(db)
        self.user_repo = UserRepository(db)

    async def onboard_employer(self, payload: EmployerCreate) -> Employer:
        existing = await self.employer_repo.get_by_registration_number(payload.registration_number)
        if existing:
            raise AlreadyExistsException("Employer with this registration number already onboarded")

        existing_user = await self.user_repo.get_by_email(payload.admin_email)
        if existing_user:
            raise AlreadyExistsException("A user with this admin email already exists")

        admin_user = await self.user_repo.create(
            email=payload.admin_email.lower(),
            phone_number=payload.admin_phone_number,
            hashed_password=hash_password(payload.admin_password),
            user_type=UserType.EMPLOYER_ADMIN,
        )
        role = await self.user_repo.get_role_by_name("EMPLOYER_ADMIN")
        if role:
            admin_user.roles.append(role)

        employer = await self.employer_repo.create(
            admin_user_id=admin_user.id,
            legal_name=payload.legal_name,
            trade_name=payload.trade_name,
            registration_number=payload.registration_number,
            gstin=payload.gstin,
            industry=payload.industry,
            employee_count_band=payload.employee_count_band,
            address=payload.address,
            city=payload.city,
            state=payload.state,
        )
        await self.db.commit()
        await self.db.refresh(employer)
        return employer

    async def get_employer_or_404(self, employer_id: uuid.UUID) -> Employer:
        employer = await self.employer_repo.get_by_id(employer_id)
        if not employer:
            raise NotFoundException("Employer not found")
        return employer

    async def create_department(self, employer_id: uuid.UUID, payload: DepartmentCreate):
        dept_repo = DepartmentRepository(self.db)
        dept = await dept_repo.create(employer_id=employer_id, name=payload.name, cost_center_code=payload.cost_center_code)
        await self.db.commit()
        return dept

    async def list_departments(self, employer_id: uuid.UUID):
        dept_repo = DepartmentRepository(self.db)
        return await dept_repo.list_for_employer(employer_id)


class EmployeeService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.employee_repo = EmployeeRepository(db)
        self.employer_repo = EmployerRepository(db)
        self.user_repo = UserRepository(db)

    async def onboard_employee(self, payload: EmployeeCreate) -> Employee:
        employer = await self.employer_repo.get_by_id(payload.employer_id)
        if not employer:
            raise NotFoundException("Employer not found")

        existing_code = await self.employee_repo.get_by_employee_code(payload.employer_id, payload.employee_code)
        if existing_code:
            raise AlreadyExistsException("An employee with this employee code already exists for this employer")

        existing_user = await self.user_repo.get_by_email(payload.email)
        if existing_user:
            raise AlreadyExistsException("A user with this email already exists")

        user = await self.user_repo.create(
            email=payload.email.lower(),
            phone_number=payload.phone_number,
            hashed_password=hash_password(payload.password),
            user_type=UserType.EMPLOYEE,
        )
        role = await self.user_repo.get_role_by_name("EMPLOYEE")
        if role:
            user.roles.append(role)

        employee = await self.employee_repo.create(
            user_id=user.id,
            employer_id=payload.employer_id,
            department_id=payload.department_id,
            employee_code=payload.employee_code,
            full_name=payload.full_name,
            designation=payload.designation,
            date_of_joining=payload.date_of_joining,
            date_of_birth=payload.date_of_birth,
            monthly_gross_salary=payload.monthly_gross_salary,
            monthly_net_salary=payload.monthly_net_salary,
            pan_encrypted=encrypt_field(payload.pan_number) if payload.pan_number else None,
            aadhaar_encrypted=encrypt_field(payload.aadhaar_number) if payload.aadhaar_number else None,
            bank_account_encrypted=encrypt_field(payload.bank_account_number) if payload.bank_account_number else None,
            ifsc_code=payload.ifsc_code,
        )
        await self.db.commit()
        await self.db.refresh(employee)
        return employee

    async def get_employee_or_404(self, employee_id: uuid.UUID) -> Employee:
        employee = await self.employee_repo.get_by_id(employee_id)
        if not employee:
            raise NotFoundException("Employee not found")
        return employee

    async def get_employee_by_user(self, user: User) -> Employee:
        employee = await self.employee_repo.get_by_user_id(user.id)
        if not employee:
            raise NotFoundException("No employee profile linked to this user")
        return employee

    async def update_employee(self, employee_id: uuid.UUID, payload: EmployeeUpdate) -> Employee:
        employee = await self.get_employee_or_404(employee_id)
        return await self.employee_repo.update(employee, **payload.model_dump(exclude_unset=True))

    async def list_for_employer(self, employer_id: uuid.UUID, offset: int = 0, limit: int = 100):
        return await self.employee_repo.list_for_employer(employer_id, offset, limit)
