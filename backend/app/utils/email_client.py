"""
Thin SMTP client wrapper. Swap this module's implementation to integrate
SES/SendGrid/Postmark without touching calling code.
"""
import smtplib
from email.mime.text import MIMEText

from app.core.config import settings
from app.core.logging_config import get_logger

logger = get_logger(__name__)


def send_email_sync(to_email: str, subject: str, body: str) -> None:
    if not settings.SMTP_HOST:
        # Development fallback: log instead of sending, so local/dev environments
        # don't require real SMTP credentials to exercise the auth flow.
        logger.info("email_dev_fallback", to=to_email, subject=subject, body=body)
        return

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = settings.SMTP_FROM
    msg["To"] = to_email

    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.starttls()
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.sendmail(settings.SMTP_FROM, [to_email], msg.as_string())
