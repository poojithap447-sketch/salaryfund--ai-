import uuid
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.financial_wellness.engine import WellnessInputs, calculate_financial_wellness
from app.core.exceptions import NotFoundException
from app.models.ai_and_wellness import FinancialWellnessRecord
from app.models.loans import EMI, EMIStatus, Loan, LoanStatus
from app.repositories.base import BaseRepository
from app.repositories.organization_repository import EmployeeRepository


class FinancialWellnessRepository(BaseRepository[FinancialWellnessRecord]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, FinancialWellnessRecord)

    async def latest_for_employee(self, employee_id: uuid.UUID) -> FinancialWellnessRecord | None:
        result = await self.db.execute(
            select(FinancialWellnessRecord)
            .where(FinancialWellnessRecord.employee_id == employee_id)
            .order_by(FinancialWellnessRecord.computed_at.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()

    async def history_for_employee(self, employee_id: uuid.UUID, limit: int = 24):
        result = await self.db.execute(
            select(FinancialWellnessRecord)
            .where(FinancialWellnessRecord.employee_id == employee_id)
            .order_by(FinancialWellnessRecord.computed_at.desc())
            .limit(limit)
        )
        return result.scalars().all()


class FinancialWellnessService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = FinancialWellnessRepository(db)
        self.employee_repo = EmployeeRepository(db)

    async def compute_and_store(self, employee_id: uuid.UUID) -> FinancialWellnessRecord:
        employee = await self.employee_repo.get_by_id(employee_id)
        if not employee:
            raise NotFoundException("Employee not found")

        loans_result = await self.db.execute(
            select(Loan).where(Loan.employee_id == employee_id, Loan.status == LoanStatus.ACTIVE)
        )
        active_loans = loans_result.scalars().all()

        total_active_principal = sum((l.outstanding_principal for l in active_loans), Decimal(0))
        total_sanctioned = sum((l.principal_amount for l in active_loans), Decimal(0))

        emi_result = await self.db.execute(
            select(EMI).join(Loan, Loan.id == EMI.loan_id).where(
                Loan.employee_id == employee_id, EMI.status.in_([EMIStatus.DUE, EMIStatus.UPCOMING])
            )
        )
        upcoming_emis = emi_result.scalars().all()
        total_monthly_debt = sum((e.emi_amount for e in upcoming_emis[:len(active_loans) or 1]), Decimal(0))

        monthly_net_salary = employee.monthly_net_salary
        essential_expenses = monthly_net_salary * Decimal("0.5")  # heuristic until real expense-tracking data exists
        estimated_savings = max(Decimal(0), monthly_net_salary - essential_expenses - total_monthly_debt)
        liquid_savings_balance = estimated_savings * 3  # heuristic proxy for accumulated reserve

        inputs = WellnessInputs(
            monthly_net_salary=float(monthly_net_salary),
            total_monthly_debt_payments=float(total_monthly_debt),
            monthly_savings=float(estimated_savings),
            total_active_loan_principal=float(total_active_principal),
            total_sanctioned_loan_limit=float(total_sanctioned) if total_sanctioned else float(monthly_net_salary) * 6,
            liquid_savings_balance=float(liquid_savings_balance),
            monthly_essential_expenses=float(essential_expenses),
        )
        result = calculate_financial_wellness(inputs)

        record = await self.repo.create(
            employee_id=employee_id,
            debt_to_income_ratio=result["debt_to_income_ratio"],
            savings_ratio=result["savings_ratio"],
            emi_burden_ratio=result["emi_burden_ratio"],
            loan_utilization_ratio=result["loan_utilization_ratio"],
            emergency_reserve_months=result["emergency_reserve_months"],
            wellness_score=result["wellness_score"],
            wellness_band=result["wellness_band"],
            recommendations=result["recommendations"],
        )
        await self.db.commit()
        await self.db.refresh(record)
        return record

    async def get_latest(self, employee_id: uuid.UUID) -> FinancialWellnessRecord:
        record = await self.repo.latest_for_employee(employee_id)
        if not record:
            record = await self.compute_and_store(employee_id)
        return record

    async def get_history(self, employee_id: uuid.UUID):
        return await self.repo.history_for_employee(employee_id)
