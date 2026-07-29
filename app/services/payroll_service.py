"""
Payroll ingestion service. Employers upload monthly payroll rows (or sync via
HRMS webhook / API) which are reconciled against active EMIs to compute
automated in-payroll loan deductions.
"""
import uuid
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundException
from app.models.loans import EMI, EMIStatus, Loan, LoanStatus
from app.models.payroll import Payroll, PayrollStatus
from app.repositories.base import BaseRepository
from app.repositories.organization_repository import EmployeeRepository
from app.schemas.ai_and_wellness import PayrollUploadRow


class PayrollRepository(BaseRepository[Payroll]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Payroll)

    async def get_for_cycle(self, employee_id: uuid.UUID, month: int, year: int) -> Payroll | None:
        result = await self.db.execute(
            select(Payroll).where(Payroll.employee_id == employee_id, Payroll.cycle_month == month, Payroll.cycle_year == year)
        )
        return result.scalar_one_or_none()

    async def list_for_employee(self, employee_id: uuid.UUID, limit: int = 12):
        result = await self.db.execute(
            select(Payroll)
            .where(Payroll.employee_id == employee_id)
            .order_by(Payroll.cycle_year.desc(), Payroll.cycle_month.desc())
            .limit(limit)
        )
        return result.scalars().all()


class PayrollService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = PayrollRepository(db)
        self.employee_repo = EmployeeRepository(db)

    async def ingest_row(self, employer_id: uuid.UUID, row: PayrollUploadRow) -> Payroll:
        employee = await self.employee_repo.get_by_employee_code(employer_id, row.employee_code)
        if not employee:
            raise NotFoundException(f"No employee found with code {row.employee_code} for this employer")

        emi_deduction = await self._compute_emi_deduction(employee.id)
        net_salary = row.gross_salary - row.deductions - emi_deduction

        existing = await self.repo.get_for_cycle(employee.id, row.cycle_month, row.cycle_year)
        if existing:
            payroll = await self.repo.update(
                existing,
                gross_salary=row.gross_salary,
                deductions=row.deductions,
                emi_deductions=emi_deduction,
                net_salary=net_salary,
                days_present=row.days_present,
                days_absent=row.days_absent,
                payment_date=row.payment_date,
                status=PayrollStatus.PROCESSED,
            )
        else:
            payroll = await self.repo.create(
                employee_id=employee.id,
                employer_id=employer_id,
                cycle_month=row.cycle_month,
                cycle_year=row.cycle_year,
                gross_salary=row.gross_salary,
                deductions=row.deductions,
                emi_deductions=emi_deduction,
                net_salary=net_salary,
                days_present=row.days_present,
                days_absent=row.days_absent,
                payment_date=row.payment_date,
                status=PayrollStatus.PROCESSED,
                source="MANUAL_UPLOAD",
            )
        await self.db.commit()
        await self.db.refresh(payroll)
        return payroll

    async def bulk_ingest(self, employer_id: uuid.UUID, rows: list[PayrollUploadRow]) -> list[Payroll]:
        results = []
        for row in rows:
            results.append(await self.ingest_row(employer_id, row))
        return results

    async def _compute_emi_deduction(self, employee_id: uuid.UUID) -> Decimal:
        """Sums EMI amounts due this cycle across all active loans for payroll deduction."""
        result = await self.db.execute(
            select(EMI)
            .join(Loan, Loan.id == EMI.loan_id)
            .where(Loan.employee_id == employee_id, Loan.status == LoanStatus.ACTIVE, EMI.status.in_([EMIStatus.DUE, EMIStatus.UPCOMING]))
        )
        due_emis = result.scalars().all()
        return sum((e.emi_amount for e in due_emis), Decimal(0))

    async def list_for_employee(self, employee_id: uuid.UUID):
        return await self.repo.list_for_employee(employee_id)
