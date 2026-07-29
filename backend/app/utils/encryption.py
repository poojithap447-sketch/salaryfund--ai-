"""
Symmetric encryption for sensitive PII fields (PAN, Aadhaar, bank account numbers)
stored at rest using Fernet (AES-128-CBC + HMAC).
"""
from cryptography.fernet import Fernet, InvalidToken

from app.core.config import settings
from app.core.exceptions import AppException

_fernet = Fernet(settings.FIELD_ENCRYPTION_KEY.encode("utf-8"))


def encrypt_field(plain_value: str) -> str:
    return _fernet.encrypt(plain_value.encode("utf-8")).decode("utf-8")


def decrypt_field(encrypted_value: str) -> str:
    try:
        return _fernet.decrypt(encrypted_value.encode("utf-8")).decode("utf-8")
    except InvalidToken as exc:
        raise AppException("Failed to decrypt sensitive field - key mismatch or data corruption") from exc


def mask_pan(pan: str) -> str:
    if len(pan) < 4:
        return "****"
    return f"{'*' * (len(pan) - 4)}{pan[-4:]}"
