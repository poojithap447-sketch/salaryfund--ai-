"""
Monthly/on-demand report generation. Reports are computed via aggregate SQL
queries and written as CSV to disk; the Report row's file_path is updated so
the REST API can serve a signed download link.
"""
import csv
import os
from datetime import datetime, timezone

from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session

from app.background_tasks.celery_app import celery_app
from app.core.config import settings
from app.core.logging_config import get_logger
from app.models.loans import Loan, LoanStatus
from app.models.ai_and_wellness import Report, ReportStatus, ReportType

logger = get_logger(__name__)
_sync_engine = create_engine(settings.DATABASE_URL_SYNC, pool_pre_ping=True)

REPORTS_DIR = "/data/reports"


@celery_app.task(name="app.background_tasks.report_tasks.generate_monthly_portfolio_report")
def generate_monthly_portfolio_report():
    os.makedirs(REPORTS_DIR, exist_ok=True)
    filename = f"portfolio_report_{datetime.now(timezone.utc).strftime('%Y%m')}.csv"
    filepath = os.path.join(REPORTS_DIR, filename)

    with Session(_sync_engine) as session:
        report = Report(
            report_type=ReportType.MONTHLY_PORTFOLIO,
            requested_by_user_id=None,
            status=ReportStatus.GENERATING,
        )
        session.add(report)
        session.commit()

        try:
            rows = session.execute(
                select(Loan.status, func.count(Loan.id), func.sum(Loan.outstanding_principal)).group_by(Loan.status)
            ).all()

            with open(filepath, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["status", "loan_count", "total_outstanding_principal"])
                for status, count, total in rows:
                    writer.writerow([status.value if hasattr(status, "value") else status, count, total or 0])

            report.status = ReportStatus.READY
            report.file_path = filepath
            session.commit()
            logger.info("monthly_report_generated", path=filepath)
        except Exception as exc:
            report.status = ReportStatus.FAILED
            report.error_message = str(exc)
            session.commit()
            logger.error("monthly_report_failed", error=str(exc))
            raise

    return {"file_path": filepath}
