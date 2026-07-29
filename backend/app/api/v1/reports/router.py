import uuid

from fastapi import APIRouter, Depends, status

from app.dependencies.auth import CurrentUser, DBSession, require_roles
from app.models.ai_and_wellness import Report, ReportStatus, ReportType
from app.repositories.base import BaseRepository

router = APIRouter(prefix="/reports", tags=["Reports"], dependencies=[Depends(require_roles("PLATFORM_ADMIN", "EMPLOYER_ADMIN"))])


class ReportRepository(BaseRepository[Report]):
    def __init__(self, db):
        super().__init__(db, Report)


@router.post("/generate", status_code=status.HTTP_202_ACCEPTED)
async def request_report(report_type: ReportType, current_user: CurrentUser, db: DBSession, employer_id: uuid.UUID | None = None):
    """Queues an async report generation job (see app.background_tasks.report_tasks)."""
    repo = ReportRepository(db)
    report = await repo.create(report_type=report_type, requested_by_user_id=current_user.id, employer_id=employer_id, status=ReportStatus.QUEUED)
    await db.commit()

    if report_type == ReportType.MONTHLY_PORTFOLIO:
        from app.background_tasks.report_tasks import generate_monthly_portfolio_report

        generate_monthly_portfolio_report.delay()

    return {"report_id": str(report.id), "status": report.status.value}


@router.get("/{report_id}")
async def get_report_status(report_id: uuid.UUID, db: DBSession):
    repo = ReportRepository(db)
    report = await repo.get_by_id(report_id)
    if not report:
        from app.core.exceptions import NotFoundException

        raise NotFoundException("Report not found")
    return {"id": str(report.id), "status": report.status.value, "file_path": report.file_path}
