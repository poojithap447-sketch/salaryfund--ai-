import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.loans import (
    EMI,
    InterestRate,
    Lender,
    Loan,
    LoanApplication,
    LoanApplicationStatus,
    LoanPolicy,
    LoanStatus,
    LoanType,
    Transaction,
)
from app.repositories.base import BaseRepository


class LoanTypeRepository(BaseRepository[LoanType]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, LoanType)

    async def get_active_policy(self, loan_type_id: uuid.UUID) -> LoanPolicy | None:
        result = await self.db.execute(
            select(LoanPolicy).where(LoanPolicy.loan_type_id == loan_type_id, LoanPolicy.is_active.is_(True))
        )
        return result.scalar_one_or_none()


class LenderRepository(BaseRepository[Lender]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Lender)

    async def get_best_rate(self, lender_id: uuid.UUID, loan_type_id: uuid.UUID, risk_band: str) -> InterestRate | None:
        today = datetime.now(timezone.utc).date()
        result = await self.db.execute(
            select(InterestRate)
            .where(
                InterestRate.lender_id == lender_id,
                InterestRate.loan_type_id == loan_type_id,
                InterestRate.risk_band == risk_band,
                InterestRate.effective_from <= today,
            )
            .order_by(InterestRate.effective_from.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()

    async def list_active(self):
        result = await self.db.execute(select(Lender).where(Lender.is_active.is_(True)))
        return result.scalars().all()


class LoanApplicationRepository(BaseRepository[LoanApplication]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, LoanApplication)

    async def list_for_employee(self, employee_id: uuid.UUID):
        result = await self.db.execute(
            select(LoanApplication).where(LoanApplication.employee_id == employee_id).order_by(LoanApplication.created_at.desc())
        )
        return result.scalars().all()

    async def count_active_loans(self, employee_id: uuid.UUID) -> int:
        result = await self.db.execute(
            select(LoanApplication).where(
                LoanApplication.employee_id == employee_id,
                LoanApplication.status.in_(
                    [LoanApplicationStatus.SUBMITTED, LoanApplicationStatus.UNDER_AI_REVIEW, LoanApplicationStatus.UNDER_MANUAL_REVIEW]
                ),
            )
        )
        return len(result.scalars().all())

    async def list_pending_review(self, offset: int = 0, limit: int = 50):
        result = await self.db.execute(
            select(LoanApplication)
            .where(LoanApplication.status == LoanApplicationStatus.UNDER_MANUAL_REVIEW)
            .order_by(LoanApplication.submitted_at.asc())
            .offset(offset)
            .limit(limit)
        )
        return result.scalars().all()


class LoanRepository(BaseRepository[Loan]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Loan)

    async def list_active_for_employee(self, employee_id: uuid.UUID):
        result = await self.db.execute(
            select(Loan).where(Loan.employee_id == employee_id, Loan.status == LoanStatus.ACTIVE)
        )
        return result.scalars().all()

    async def get_by_application_id(self, application_id: uuid.UUID) -> Loan | None:
        result = await self.db.execute(select(Loan).where(Loan.application_id == application_id))
        return result.scalar_one_or_none()


class EMIRepository(BaseRepository[EMI]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, EMI)

    async def list_for_loan(self, loan_id: uuid.UUID):
        result = await self.db.execute(select(EMI).where(EMI.loan_id == loan_id).order_by(EMI.installment_number))
        return result.scalars().all()

    async def list_due_between(self, start, end):
        result = await self.db.execute(select(EMI).where(EMI.due_date.between(start, end)))
        return result.scalars().all()


class TransactionRepository(BaseRepository[Transaction]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Transaction)

    async def list_for_employee(self, employee_id: uuid.UUID, offset: int = 0, limit: int = 100):
        result = await self.db.execute(
            select(Transaction).where(Transaction.employee_id == employee_id).order_by(Transaction.created_at.desc()).offset(offset).limit(limit)
        )
        return result.scalars().all()
