import uuid
from datetime import date, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.career_credit.engine import CareerScoreInputs, calculate_career_score
from app.core.exceptions import NotFoundException
from app.models.ai_and_wellness import CareerCreditScore
from app.models.loans import EMI, EMIStatus, Loan
from app.models.payroll import Payroll
from app.repositories.base import BaseRepository
from app.repositories.organization_repository import EmployeeRepository


class CareerScoreRepository(BaseRepository[CareerCreditScore]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, CareerCreditScore)

    async def latest_for_employee(self, employee_id: uuid.UUID) -> CareerCreditScore | None:
        result = await self.db.execute(
            select(CareerCreditScore)
            .where(CareerCreditScore.employee_id == employee_id)
            .order_by(CareerCreditScore.computed_at.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()

    async def history_for_employee(self, employee_id: uuid.UUID, limit: int = 24):
        result = await self.db.execute(
            select(CareerCreditScore)
            .where(CareerCreditScore.employee_id == employee_id)
            .order_by(CareerCreditScore.computed_at.desc())
            .limit(limit)
        )
        return result.scalars().all()


class CareerScoreService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = CareerScoreRepository(db)
        self.employee_repo = EmployeeRepository(db)

    async def compute_and_store(self, employee_id: uuid.UUID) -> CareerCreditScore:
        employee = await self.employee_repo.get_by_id(employee_id)
        if not employee:
            raise NotFoundException("Employee not found")

        tenure_months = self._months_between(employee.date_of_joining, date.today())

        # Repayment behavior derived from actual EMI history
        emi_result = await self.db.execute(
            select(EMI).join(Loan, Loan.id == EMI.loan_id).where(Loan.employee_id == employee_id)
        )
        emis = emi_result.scalars().all()
        total_emis = len(emis)
        on_time = sum(1 for e in emis if e.status == EMIStatus.PAID and (e.paid_at is None or e.paid_at.date() <= e.due_date))
        defaults = sum(1 for e in emis if e.status == EMIStatus.OVERDUE)

        # Attendance / performance from most recent payroll records (proxy until dedicated HRMS feed exists)
        payroll_result = await self.db.execute(
            select(Payroll).where(Payroll.employee_id == employee_id).order_by(Payroll.cycle_year.desc(), Payroll.cycle_month.desc()).limit(6)
        )
        recent_payrolls = payroll_result.scalars().all()
        if recent_payrolls:
            avg_attendance = sum(
                (p.days_present or 22) / max((p.days_present or 22) + (p.days_absent or 0), 1) * 100 for p in recent_payrolls
            ) / len(recent_payrolls)
            salary_growth = self._salary_growth_pct(recent_payrolls)
        else:
            avg_attendance = 90.0
            salary_growth = 0.0

        inputs = CareerScoreInputs(
            tenure_months=tenure_months,
            number_of_employers_last_5_years=1,
            salary_growth_pct_yoy=salary_growth,
            attendance_pct=avg_attendance,
            promotions_count=0,
            tenure_years_total=tenure_months / 12,
            performance_rating=3.5,
            on_time_emi_payments=on_time,
            total_emi_payments=total_emis,
            num_defaults=defaults,
        )
        result = calculate_career_score(inputs)

        record = await self.repo.create(
            employee_id=employee_id,
            score=result["score"],
            band=result["band"],
            employment_stability_score=result["employment_stability_score"],
            salary_growth_score=result["salary_growth_score"],
            attendance_score=result["attendance_score"],
            promotion_score=result["promotion_score"],
            performance_score=result["performance_score"],
            repayment_behavior_score=result["repayment_behavior_score"],
            feature_breakdown=result["feature_breakdown"],
        )
        await self.db.commit()
        await self.db.refresh(record)
        return record

    async def get_latest(self, employee_id: uuid.UUID) -> CareerCreditScore:
        record = await self.repo.latest_for_employee(employee_id)
        if not record:
            record = await self.compute_and_store(employee_id)
        return record

    async def get_history(self, employee_id: uuid.UUID):
        return await self.repo.history_for_employee(employee_id)

    @staticmethod
    def _months_between(start: date, end: date) -> float:
        return (end.year - start.year) * 12 + (end.month - start.month)

    @staticmethod
    def _salary_growth_pct(payrolls: list[Payroll]) -> float:
        if len(payrolls) < 2:
            return 0.0
        newest, oldest = payrolls[0], payrolls[-1]
        if oldest.gross_salary == 0:
            return 0.0
        return float((newest.gross_salary - oldest.gross_salary) / oldest.gross_salary * 100)
