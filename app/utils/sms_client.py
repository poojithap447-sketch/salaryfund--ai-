"""
Thin SMS gateway client wrapper (provider-agnostic: MSG91 / Twilio / SNS).
Uses requests-free implementation; wire up the real provider's HTTP API here.
"""
import httpx

from app.core.config import settings
from app.core.logging_config import get_logger

logger = get_logger(__name__)


def send_sms_sync(to_phone: str, message: str) -> None:
    if not settings.SMS_PROVIDER_API_KEY:
        logger.info("sms_dev_fallback", to=to_phone, message=message)
        return

    # Example generic REST SMS gateway call - replace URL/payload with your provider's spec.
    with httpx.Client(timeout=10) as client:
        response = client.post(
            "https://api.sms-provider.example.com/v1/send",
            headers={"Authorization": f"Bearer {settings.SMS_PROVIDER_API_KEY}"},
            json={"to": to_phone, "message": message, "sender_id": settings.SMS_PROVIDER_SENDER_ID},
        )
        response.raise_for_status()
