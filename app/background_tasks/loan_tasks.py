"""
Loan lifecycle background jobs: daily EMI due-date reminders and overdue marking.
Uses a synchronous SQLAlchemy session (Celery workers run outside the FastAPI
async event loop) via a dedicated sync engine built from DATABASE_URL_SYNC.
"""
from datetime import date, timedelta

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from app.background_tasks.celery_app import celery_app
from app.background_tasks.notification_tasks import send_email_task
from app.core.config import settings
from app.core.logging_config import get_logger
from app.models.loans import EMI, EMIStatus, Loan
from app.models.organization import Employee
from app.models.rbac import User

logger = get_logger(__name__)
_sync_engine = create_engine(settings.DATABASE_URL_SYNC, pool_pre_ping=True)


@celery_app.task(name="app.background_tasks.loan_tasks.send_emi_reminders")
def send_emi_reminders():
    reminder_window_end = date.today() + timedelta(days=3)
    with Session(_sync_engine) as session:
        stmt = (
            select(EMI, Loan, Employee, User)
            .join(Loan, Loan.id == EMI.loan_id)
            .join(Employee, Employee.id == Loan.employee_id)
            .join(User, User.id == Employee.user_id)
            .where(EMI.status.in_([EMIStatus.UPCOMING, EMIStatus.DUE]), EMI.due_date.between(date.today(), reminder_window_end))
        )
        rows = session.execute(stmt).all()
        count = 0
        for emi, loan, employee, user in rows:
            send_email_task.delay(
                to_email=user.email,
                subject="Upcoming EMI Payment Reminder - SalaryFund AI",
                body=(
                    f"Dear {employee.full_name}, your EMI of INR {emi.emi_amount} for loan "
                    f"{loan.id} is due on {emi.due_date}. Please ensure sufficient balance."
                ),
            )
            count += 1
        logger.info("emi_reminders_dispatched", count=count)
        return {"reminders_sent": count}


@celery_app.task(name="app.background_tasks.loan_tasks.mark_overdue_emis")
def mark_overdue_emis():
    with Session(_sync_engine) as session:
        stmt = select(EMI).where(EMI.status.in_([EMIStatus.UPCOMING, EMIStatus.DUE]), EMI.due_date < date.today())
        overdue = session.execute(stmt).scalars().all()
        for emi in overdue:
            emi.status = EMIStatus.OVERDUE
            days_late = (date.today() - emi.due_date).days
            emi.late_fee = round(float(emi.emi_amount) * 0.02 * min(days_late, 30) / 30, 2)
        session.commit()
        logger.info("emis_marked_overdue", count=len(overdue))
        return {"overdue_count": len(overdue)}
