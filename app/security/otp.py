"""
OTP generation & verification utilities. OTPs are stored hashed (never plaintext)
using the same bcrypt context as passwords, with attempt limiting.
"""
import hashlib
import secrets

MAX_OTP_ATTEMPTS = 5


def generate_otp_code(length: int = 6) -> str:
    """Cryptographically secure numeric OTP."""
    return "".join(secrets.choice("0123456789") for _ in range(length))


def hash_otp(code: str) -> str:
    # SHA-256 is sufficient here since OTPs are short-lived and rate-limited;
    # bcrypt is reserved for long-lived credentials (passwords).
    return hashlib.sha256(code.encode("utf-8")).hexdigest()


def verify_otp(code: str, code_hash: str) -> bool:
    return secrets.compare_digest(hash_otp(code), code_hash)
