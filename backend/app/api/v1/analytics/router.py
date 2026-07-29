import uuid

from fastapi import APIRouter, Depends
from sqlalchemy import func, select

from app.dependencies.auth import DBSession, require_roles
from app.models.loans import Loan, LoanApplication, LoanApplicationStatus, LoanStatus
from app.models.organization import Employee, Employer

router = APIRouter(prefix="/analytics", tags=["Analytics"], dependencies=[Depends(require_roles("PLATFORM_ADMIN", "EMPLOYER_ADMIN"))])


@router.get("/portfolio-summary")
async def portfolio_summary(db: DBSession):
    """Platform-wide loan portfolio KPIs: counts and outstanding principal by status."""
    result = await db.execute(select(Loan.status, func.count(Loan.id), func.sum(Loan.outstanding_principal)).group_by(Loan.status))
    rows = result.all()
    return {
        "by_status": [
            {"status": status.value, "count": count, "total_outstanding": float(total or 0)} for status, count, total in rows
        ]
    }


@router.get("/application-funnel")
async def application_funnel(db: DBSession):
    """Application status funnel - useful for conversion-rate dashboards."""
    result = await db.execute(select(LoanApplication.status, func.count(LoanApplication.id)).group_by(LoanApplication.status))
    return {"funnel": [{"status": status.value, "count": count} for status, count in result.all()]}


@router.get("/employer/{employer_id}/utilization")
async def employer_utilization(employer_id: uuid.UUID, db: DBSession):
    """Employer-level utilization: how many employees have active loans vs total headcount."""
    total_employees = (await db.execute(select(func.count(Employee.id)).where(Employee.employer_id == employer_id))).scalar_one()
    active_borrowers = (
        await db.execute(
            select(func.count(func.distinct(Loan.employee_id)))
            .select_from(Loan)
            .join(Employee, Employee.id == Loan.employee_id)
            .where(Employee.employer_id == employer_id, Loan.status == LoanStatus.ACTIVE)
        )
    ).scalar_one()
    return {
        "employer_id": str(employer_id),
        "total_employees": total_employees,
        "active_borrowers": active_borrowers,
        "utilization_pct": round((active_borrowers / total_employees * 100), 2) if total_employees else 0,
    }
