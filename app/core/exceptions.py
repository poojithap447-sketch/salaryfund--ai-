"""
Application-wide exception hierarchy.
Every domain error inherits from AppException so the global exception handler
(registered in app/main.py) can map it to a consistent JSON error response.
"""
from typing import Any, Optional


class AppException(Exception):
    status_code: int = 400
    error_code: str = "APP_ERROR"

    def __init__(self, message: str, error_code: Optional[str] = None, details: Optional[Any] = None):
        self.message = message
        self.error_code = error_code or self.error_code
        self.details = details
        super().__init__(message)


class NotFoundException(AppException):
    status_code = 404
    error_code = "NOT_FOUND"


class AlreadyExistsException(AppException):
    status_code = 409
    error_code = "ALREADY_EXISTS"


class ValidationException(AppException):
    status_code = 422
    error_code = "VALIDATION_ERROR"


class UnauthorizedException(AppException):
    status_code = 401
    error_code = "UNAUTHORIZED"


class ForbiddenException(AppException):
    status_code = 403
    error_code = "FORBIDDEN"


class InvalidCredentialsException(UnauthorizedException):
    error_code = "INVALID_CREDENTIALS"


class TokenExpiredException(UnauthorizedException):
    error_code = "TOKEN_EXPIRED"


class InvalidTokenException(UnauthorizedException):
    error_code = "INVALID_TOKEN"


class OTPException(AppException):
    status_code = 400
    error_code = "OTP_ERROR"


class RateLimitException(AppException):
    status_code = 429
    error_code = "RATE_LIMITED"


class FraudSuspectedException(AppException):
    status_code = 403
    error_code = "FRAUD_SUSPECTED"


class InsufficientEligibilityException(AppException):
    status_code = 422
    error_code = "INELIGIBLE"


class FileUploadException(AppException):
    status_code = 400
    error_code = "FILE_UPLOAD_ERROR"


class AIModelException(AppException):
    status_code = 500
    error_code = "AI_MODEL_ERROR"
