"""
Email / SMS delivery background tasks.
Providers (SMTP, SMS gateway) are abstracted behind app.utils.email_client / sms_client
so swapping providers (SES, Twilio, MSG91, etc.) doesn't touch task logic.
"""
from app.background_tasks.celery_app import celery_app
from app.core.logging_config import get_logger
from app.utils.email_client import send_email_sync
from app.utils.sms_client import send_sms_sync

logger = get_logger(__name__)


@celery_app.task(name="app.background_tasks.notification_tasks.send_email_task", bind=True, max_retries=3, default_retry_delay=30)
def send_email_task(self, to_email: str, subject: str, body: str):
    try:
        send_email_sync(to_email=to_email, subject=subject, body=body)
        logger.info("email_sent", to=to_email, subject=subject)
    except Exception as exc:
        logger.error("email_send_failed", to=to_email, error=str(exc))
        raise self.retry(exc=exc)


@celery_app.task(name="app.background_tasks.notification_tasks.send_sms_task", bind=True, max_retries=3, default_retry_delay=30)
def send_sms_task(self, to_phone: str, message: str):
    try:
        send_sms_sync(to_phone=to_phone, message=message)
        logger.info("sms_sent", to=to_phone)
    except Exception as exc:
        logger.error("sms_send_failed", to=to_phone, error=str(exc))
        raise self.retry(exc=exc)
