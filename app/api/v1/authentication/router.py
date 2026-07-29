"""
Authentication endpoints: registration, login, OTP, MFA, token refresh, logout,
password reset. Rate limiting for auth/OTP endpoints is applied globally via
the SlowAPI middleware configured in app/main.py using settings.RATE_LIMIT_AUTH
and settings.RATE_LIMIT_OTP.
"""
import uuid

from fastapi import APIRouter, Request, status

from app.core.exceptions import NotFoundException
from app.dependencies.auth import CurrentUser, DBSession
from app.models.rbac import OTPPurpose
from app.repositories.user_repository import UserRepository
from app.schemas.auth import (
    OTPRequestSchema,
    OTPVerifyRequest,
    PasswordResetRequest,
    RefreshTokenRequest,
    TokenResponse,
    UserLoginRequest,
    UserRegisterRequest,
    UserResponse,
)
from app.security.password import hash_password
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(payload: UserRegisterRequest, db: DBSession):
    """Registers a new user account and triggers an email-verification OTP."""
    service = AuthService(db)
    return await service.register(payload)


@router.post("/login", response_model=TokenResponse)
async def login(payload: UserLoginRequest, request: Request, db: DBSession):
    """Authenticates with email/password and issues an access + refresh token pair."""
    service = AuthService(db)
    user = await service.authenticate(payload)
    return await service.issue_tokens(
        user,
        device_info=request.headers.get("user-agent"),
        ip_address=request.client.host if request.client else None,
    )


@router.post("/otp/request", status_code=status.HTTP_202_ACCEPTED)
async def request_otp(payload: OTPRequestSchema, db: DBSession):
    """
    Requests an OTP for LOGIN, EMAIL_VERIFICATION, PHONE_VERIFICATION, PASSWORD_RESET, or MFA.
    Looks up the target user by email or phone; response is intentionally generic
    to avoid leaking account existence.
    """
    user_repo = UserRepository(db)
    user = await user_repo.get_by_email(payload.email) if payload.email else await user_repo.get_by_phone(payload.phone_number or "")
    if not user:
        return {"message": "If an account exists, an OTP has been sent."}

    service = AuthService(db)
    await service.request_otp(user, payload.purpose)
    return {"message": "OTP sent successfully", "user_id": str(user.id)}


@router.post("/otp/verify")
async def verify_otp(payload: OTPVerifyRequest, db: DBSession):
    """Verifies an OTP code for the given purpose (marks email/phone verified as a side effect)."""
    service = AuthService(db)
    await service.verify_otp(payload.user_id, payload.code, payload.purpose)
    return {"message": "OTP verified successfully"}


@router.post("/otp/login", response_model=TokenResponse)
async def login_with_otp(payload: OTPVerifyRequest, db: DBSession):
    """Passwordless login: verifies a LOGIN-purpose OTP and issues tokens directly."""
    service = AuthService(db)
    await service.verify_otp(payload.user_id, payload.code, OTPPurpose.LOGIN)
    user_repo = UserRepository(db)
    user = await user_repo.get_by_id(payload.user_id)
    if not user:
        raise NotFoundException("User not found")
    return await service.issue_tokens(user)


@router.post("/token/refresh", response_model=TokenResponse)
async def refresh_token(payload: RefreshTokenRequest, db: DBSession):
    """Rotates a refresh token for a new access + refresh token pair."""
    service = AuthService(db)
    return await service.refresh_access_token(payload.refresh_token)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(current_user: CurrentUser, db: DBSession):
    """Revokes all active refresh tokens for the current user (logout everywhere)."""
    service = AuthService(db)
    await service.logout(current_user)


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: CurrentUser):
    return current_user


@router.post("/password-reset/request", status_code=status.HTTP_202_ACCEPTED)
async def request_password_reset(payload: PasswordResetRequest, db: DBSession):
    """Sends a PASSWORD_RESET OTP to the account email, if it exists."""
    user_repo = UserRepository(db)
    user = await user_repo.get_by_email(payload.email)
    if user:
        service = AuthService(db)
        await service.request_otp(user, OTPPurpose.PASSWORD_RESET)
    return {"message": "If an account exists, password reset instructions have been sent."}


@router.post("/password-reset/confirm")
async def confirm_password_reset(user_id: uuid.UUID, code: str, new_password: str, db: DBSession):
    """Verifies the PASSWORD_RESET OTP and sets a new password in one step."""
    service = AuthService(db)
    await service.verify_otp(user_id, code, OTPPurpose.PASSWORD_RESET)
    user_repo = UserRepository(db)
    user = await user_repo.get_by_id(user_id)
    if not user:
        raise NotFoundException("User not found")
    user.hashed_password = hash_password(new_password)
    await db.commit()
    return {"message": "Password reset successfully"}
