"""
Comprehensive seed script for SalaryFund AI platform:
- Roles & Permissions
- Loan Types & Policies
- Demo Lender & Risk Interest Rates
- 1 HR (Employer Admin) account & Employer ("Acme Corp")
- 2 Employee accounts (John Doe, Jane Smith) with profiles
- 1 NBFC (Lender) account
- 1 Platform Admin account

Run with: python -m app.database.seeds.seed_data
"""
import asyncio
from datetime import date
from decimal import Decimal

from sqlalchemy import select

from app.core.logging_config import get_logger
from app.database.session import AsyncSessionLocal
from app.models.loans import InterestRate, Lender, LoanPolicy, LoanType, LoanTypeCode
from app.models.organization import Department, Employee, Employer, EmployerStatus, EmploymentStatus
from app.models.rbac import Permission, Role, User, UserType
from app.security.password import hash_password

logger = get_logger(__name__)

ROLES = ["PLATFORM_ADMIN", "EMPLOYER_ADMIN", "EMPLOYEE", "LENDER", "SUPPORT"]

PERMISSIONS = [
    "loans:approve", "loans:reject", "loans:disburse", "loans:view_all",
    "employees:manage", "employers:manage", "fraud:review", "reports:generate",
    "admin:full_access",
]

LOAN_TYPES = [
    dict(code=LoanTypeCode.SALARY_ADVANCE, name="Salary Advance", min_amount=1000, max_amount=50000, min_tenure_months=1, max_tenure_months=3),
    dict(code=LoanTypeCode.PERSONAL_LOAN, name="Personal Loan", min_amount=10000, max_amount=500000, min_tenure_months=3, max_tenure_months=36),
    dict(code=LoanTypeCode.EMERGENCY_LOAN, name="Emergency Loan", min_amount=1000, max_amount=25000, min_tenure_months=1, max_tenure_months=6),
    dict(code=LoanTypeCode.EDUCATION_LOAN, name="Education Loan", min_amount=20000, max_amount=1000000, min_tenure_months=6, max_tenure_months=60),
    dict(code=LoanTypeCode.MEDICAL_LOAN, name="Medical Loan", min_amount=5000, max_amount=200000, min_tenure_months=3, max_tenure_months=24),
]

DEFAULT_PASSWORD = "Password@123"


async def seed():
    async with AsyncSessionLocal() as db:
        print("1. Seeding Roles...")
        existing_roles = (await db.execute(select(Role.name))).scalars().all()
        for name in ROLES:
            if name not in existing_roles:
                db.add(Role(name=name, description=f"{name} role"))
        await db.commit()

        print("2. Seeding Permissions...")
        existing_perms = (await db.execute(select(Permission.code))).scalars().all()
        for code in PERMISSIONS:
            if code not in existing_perms:
                db.add(Permission(code=code, description=code.replace(":", " ").replace("_", " ").title()))
        await db.commit()

        admin_role = (await db.execute(select(Role).where(Role.name == "PLATFORM_ADMIN"))).scalar_one()
        all_perms = (await db.execute(select(Permission))).scalars().all()
        admin_role.permissions = all_perms
        await db.commit()

        # Load role mappings
        role_map = {}
        for r_name in ROLES:
            role_map[r_name] = (await db.execute(select(Role).where(Role.name == r_name))).scalar_one()

        print("3. Seeding Loan Types & Policies...")
        for lt_data in LOAN_TYPES:
            existing = (await db.execute(select(LoanType).where(LoanType.code == lt_data["code"]))).scalar_one_or_none()
            if not existing:
                loan_type = LoanType(**lt_data)
                db.add(loan_type)
                await db.flush()
                db.add(LoanPolicy(loan_type_id=loan_type.id))
        await db.commit()

        print("4. Seeding Demo Lender (SalaryFund Capital Partners)...")
        lender = (await db.execute(select(Lender).where(Lender.name == "SalaryFund Capital Partners"))).scalar_one_or_none()
        if not lender:
            lender = Lender(
                name="SalaryFund Capital Partners",
                license_number="NBFC-DEMO-0001",
                contact_email="lending@salaryfund.ai",
                max_exposure_limit=Decimal("100000000.00"),
            )
            db.add(lender)
            await db.flush()

            loan_types = (await db.execute(select(LoanType))).scalars().all()
            risk_bands = {"A": Decimal("10.5"), "B": Decimal("14.0"), "C": Decimal("18.5"), "D": Decimal("24.0")}
            for lt in loan_types:
                for band, rate in risk_bands.items():
                    db.add(
                        InterestRate(
                            lender_id=lender.id,
                            loan_type_id=lt.id,
                            risk_band=band,
                            annual_rate_pct=rate,
                            processing_fee_pct=Decimal("1.5"),
                            effective_from=date.today(),
                        )
                    )
            await db.commit()

        print("5. Seeding Accounts (1 HR, 2 Employees, 1 Lender, 1 Admin)...")
        pwd_hash = hash_password(DEFAULT_PASSWORD)

        # 5a. HR Account & Employer Organization
        hr_user = (await db.execute(select(User).where(User.email == "hr@acme.com"))).scalar_one_or_none()
        if not hr_user:
            hr_user = User(
                email="hr@acme.com",
                phone_number="9800000001",
                hashed_password=pwd_hash,
                user_type=UserType.EMPLOYER_ADMIN,
                is_active=True,
                is_email_verified=True,
                is_phone_verified=True,
                roles=[role_map["EMPLOYER_ADMIN"]],
            )
            db.add(hr_user)
            await db.flush()

            employer = Employer(
                admin_user_id=hr_user.id,
                legal_name="Acme Corporation Pvt Ltd",
                trade_name="Acme Corp",
                registration_number="REG-ACME-001",
                gstin="27AAACA1234A1Z5",
                industry="Technology & Financial Services",
                employee_count_band="100-500",
                status=EmployerStatus.ACTIVE,
                payroll_cycle_day=1,
                max_salary_advance_pct=Decimal("50.00"),
                city="Mumbai",
                state="Maharashtra",
            )
            db.add(employer)
            await db.flush()

            dept = Department(employer_id=employer.id, name="Engineering & Product", cost_center_code="ENG-01")
            db.add(dept)
            await db.flush()
        else:
            employer = (await db.execute(select(Employer).where(Employer.admin_user_id == hr_user.id))).scalar_one()
            dept = (await db.execute(select(Department).where(Department.employer_id == employer.id))).scalars().first()

        await db.commit()

        # 5b. Employee Account 1: John Doe
        emp1_user = (await db.execute(select(User).where(User.email == "john.doe@acme.com"))).scalar_one_or_none()
        if not emp1_user:
            emp1_user = User(
                email="john.doe@acme.com",
                phone_number="9876543210",
                hashed_password=pwd_hash,
                user_type=UserType.EMPLOYEE,
                is_active=True,
                is_email_verified=True,
                is_phone_verified=True,
                roles=[role_map["EMPLOYEE"]],
            )
            db.add(emp1_user)
            await db.flush()

            emp1_profile = Employee(
                user_id=emp1_user.id,
                employer_id=employer.id,
                department_id=dept.id if dept else None,
                employee_code="EMP001",
                full_name="John Doe",
                designation="Senior Software Engineer",
                date_of_joining=date(2022, 5, 15),
                date_of_birth=date(1994, 8, 12),
                employment_status=EmploymentStatus.ACTIVE,
                monthly_gross_salary=Decimal("120000.00"),
                monthly_net_salary=Decimal("95000.00"),
                ifsc_code="HDFC0001234",
                is_kyc_verified=True,
            )
            db.add(emp1_profile)

        # 5c. Employee Account 2: Jane Smith
        emp2_user = (await db.execute(select(User).where(User.email == "jane.smith@acme.com"))).scalar_one_or_none()
        if not emp2_user:
            emp2_user = User(
                email="jane.smith@acme.com",
                phone_number="9876543211",
                hashed_password=pwd_hash,
                user_type=UserType.EMPLOYEE,
                is_active=True,
                is_email_verified=True,
                is_phone_verified=True,
                roles=[role_map["EMPLOYEE"]],
            )
            db.add(emp2_user)
            await db.flush()

            emp2_profile = Employee(
                user_id=emp2_user.id,
                employer_id=employer.id,
                department_id=dept.id if dept else None,
                employee_code="EMP002",
                full_name="Jane Smith",
                designation="Lead Product Manager",
                date_of_joining=date(2021, 3, 1),
                date_of_birth=date(1992, 11, 24),
                employment_status=EmploymentStatus.ACTIVE,
                monthly_gross_salary=Decimal("150000.00"),
                monthly_net_salary=Decimal("120000.00"),
                ifsc_code="ICIC0005678",
                is_kyc_verified=True,
            )
            db.add(emp2_profile)

        # 5d. NBFC Account (Lender)
        lender_user = (await db.execute(select(User).where(User.email == "lender@salaryfund.ai"))).scalar_one_or_none()
        if not lender_user:
            lender_user = User(
                email="lender@salaryfund.ai",
                phone_number="9800000002",
                hashed_password=pwd_hash,
                user_type=UserType.LENDER,
                is_active=True,
                is_email_verified=True,
                is_phone_verified=True,
                roles=[role_map["LENDER"]],
            )
            db.add(lender_user)

        # 5e. Platform Admin Account
        admin_user = (await db.execute(select(User).where(User.email == "admin@salaryfund.ai"))).scalar_one_or_none()
        if not admin_user:
            admin_user = User(
                email="admin@salaryfund.ai",
                phone_number="9800000000",
                hashed_password=pwd_hash,
                user_type=UserType.PLATFORM_ADMIN,
                is_active=True,
                is_email_verified=True,
                is_phone_verified=True,
                roles=[role_map["PLATFORM_ADMIN"]],
            )
            db.add(admin_user)

        await db.commit()

        print("\n=======================================================")
        print(" SUCCESS! Seed data & Demo Accounts created in Neon DB:")
        print(" - HR Account: hr@acme.com (Pass: Password@123)")
        print(" - Employee 1: john.doe@acme.com (Pass: Password@123)")
        print(" - Employee 2: jane.smith@acme.com (Pass: Password@123)")
        print(" - NBFC Account: lender@salaryfund.ai (Pass: Password@123)")
        print(" - Admin Account: admin@salaryfund.ai (Pass: Password@123)")
        print("=======================================================\n")


if __name__ == "__main__":
    asyncio.run(seed())
