"""Unit tests for password hashing, JWT, and OTP security utilities."""
import pytest

from app.core.exceptions import InvalidTokenException, TokenExpiredException
from app.security.jwt_handler import create_access_token, create_refresh_token, decode_access_token, decode_refresh_token
from app.security.otp import generate_otp_code, hash_otp, verify_otp
from app.security.password import hash_password, verify_password


def test_password_hash_and_verify_roundtrip():
    hashed = hash_password("MySecurePass1!")
    assert hashed != "MySecurePass1!"
    assert verify_password("MySecurePass1!", hashed) is True
    assert verify_password("WrongPassword", hashed) is False


def test_jwt_access_token_roundtrip():
    token = create_access_token("user-123", ["EMPLOYEE"], "EMPLOYEE")
    payload = decode_access_token(token)
    assert payload["sub"] == "user-123"
    assert payload["roles"] == ["EMPLOYEE"]
    assert payload["type"] == "access"


def test_jwt_refresh_token_rejected_as_access_token():
    token = create_refresh_token("user-123")
    with pytest.raises(InvalidTokenException):
        decode_access_token(token)


def test_jwt_garbage_token_raises_invalid():
    with pytest.raises(InvalidTokenException):
        decode_access_token("not-a-real-token")


def test_otp_generation_and_verification():
    code = generate_otp_code()
    assert len(code) == 6
    assert code.isdigit()
    hashed = hash_otp(code)
    assert verify_otp(code, hashed) is True
    assert verify_otp("000000", hashed) is False
