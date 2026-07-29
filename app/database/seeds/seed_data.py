"""
Idempotent seed script: roles, permissions, loan types, loan policies, and a
demo lender + interest rates so the platform is immediately usable after
`alembic upgrade head`.

Run with: python -m app.database.seeds.seed_data
"""
import asyncio
from datetime import date
from decimal import Decimal

from sqlalchemy import select

from app.core.logging_config import get_logger
from app.database.session import AsyncSessionLocal
from app.models.loans import InterestRate, Lender, LoanPolicy, LoanType, LoanTypeCode
from app.models.rbac import Permission, Role

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


async def seed():
    async with AsyncSessionLocal() as db:
        # --- Roles ---
        existing_roles = (await db.execute(select(Role.name))).scalars().all()
        for name in ROLES:
            if name not in existing_roles:
                db.add(Role(name=name, description=f"{name} role"))
        await db.commit()

        # --- Permissions + attach all to PLATFORM_ADMIN ---
        existing_perms = (await db.execute(select(Permission.code))).scalars().all()
        for code in PERMISSIONS:
            if code not in existing_perms:
                db.add(Permission(code=code, description=code.replace(":", " ").replace("_", " ").title()))
        await db.commit()

        admin_role = (await db.execute(select(Role).where(Role.name == "PLATFORM_ADMIN"))).scalar_one()
        all_perms = (await db.execute(select(Permission))).scalars().all()
        admin_role.permissions = all_perms
        await db.commit()

        # --- Loan types + default policies ---
        for lt_data in LOAN_TYPES:
            existing = (await db.execute(select(LoanType).where(LoanType.code == lt_data["code"]))).scalar_one_or_none()
            if not existing:
                loan_type = LoanType(**lt_data)
                db.add(loan_type)
                await db.flush()
                db.add(LoanPolicy(loan_type_id=loan_type.id))
        await db.commit()

        # --- Demo lender + interest rates across risk bands ---
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

        logger.info("seed_complete")
        print("Seed data applied successfully.")


if __name__ == "__main__":
    asyncio.run(seed())
