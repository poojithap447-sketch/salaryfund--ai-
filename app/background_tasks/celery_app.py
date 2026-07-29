"""
Celery application factory. Broker/backend = Redis.
Beat schedule defines all recurring jobs (EMI reminders, score recalculation,
payroll sync, AI retraining, monthly reports).
"""
from celery import Celery
from celery.schedules import crontab

from app.core.config import settings

celery_app = Celery(
    "salaryfund_ai",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=[
        "app.background_tasks.notification_tasks",
        "app.background_tasks.loan_tasks",
        "app.background_tasks.ai_tasks",
        "app.background_tasks.payroll_tasks",
        "app.background_tasks.report_tasks",
    ],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Kolkata",
    enable_utc=True,
    task_track_started=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    result_expires=86400,
)

celery_app.conf.beat_schedule = {
    "send-emi-reminders-daily": {
        "task": "app.background_tasks.loan_tasks.send_emi_reminders",
        "schedule": crontab(hour=9, minute=0),
    },
    "mark-overdue-emis-daily": {
        "task": "app.background_tasks.loan_tasks.mark_overdue_emis",
        "schedule": crontab(hour=1, minute=0),
    },
    "recalculate-career-scores-weekly": {
        "task": "app.background_tasks.ai_tasks.recalculate_all_career_scores",
        "schedule": crontab(day_of_week=1, hour=2, minute=0),
    },
    "recalculate-financial-wellness-weekly": {
        "task": "app.background_tasks.ai_tasks.recalculate_all_financial_wellness",
        "schedule": crontab(day_of_week=1, hour=3, minute=0),
    },
    "retrain-eligibility-model-monthly": {
        "task": "app.background_tasks.ai_tasks.retrain_eligibility_model",
        "schedule": crontab(day_of_month=1, hour=4, minute=0),
    },
    "retrain-fraud-model-monthly": {
        "task": "app.background_tasks.ai_tasks.retrain_fraud_model",
        "schedule": crontab(day_of_month=1, hour=5, minute=0),
    },
    "generate-monthly-reports": {
        "task": "app.background_tasks.report_tasks.generate_monthly_portfolio_report",
        "schedule": crontab(day_of_month=1, hour=6, minute=0),
    },
}
