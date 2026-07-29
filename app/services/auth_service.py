"""
Authentication service: registration, login, OTP issuance/verification, token
refresh/rotation, password reset. All business logic lives here; API layer stays thin.
"""
import hashlib
import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.exceptions import (
    ForbiddenException,
    InvalidCredentialsException,
    InvalidTokenException,
    NotFoundException,
    OTPException,
)
from app.models.rbac import OTP, OTPPurpose, RefreshToken, User, UserType
from app.repositories.user_repository import OTPRepository, RefreshTokenRepository, UserRepository
from app.schemas.auth import UserLoginRequest, UserRegisterRequest
from app.security.jwt_handler import create_access_token, create_refresh_token, decode_refresh_token
from app.security.otp import MAX_OTP_ATTEMPTS, generate_otp_code, hash_otp, verify_otp
from app.security.password import hash_password, verify_password
from app.background_tasks.notification_tasks import send_email_task, send_sms_task

MAX_FAILED_LOGIN_ATTEMPTS = 5
LOCKOUT_MINUTES = 15


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)
        self.refresh_repo = RefreshTokenRepository(db)
        self.otp_repo = OTPRepository(db)

    async def register(self, payload: UserRegisterRequest) -> User:
        existing = await self.user_repo.get_by_email(payload.email)
        if existing:
            from app.core.exceptions import AlreadyExistsException

            raise AlreadyExistsException("A user with this email already exists")

        user = await self.user_repo.create(
            email=payload.email.lower(),
            phone_number=payload.phone_number,
            hashed_password=hash_password(payload.password),
            user_type=payload.user_type,
        )

        default_role_name = self._default_role_for_user_type(payload.user_type)
        role = await self.user_repo.get_role_by_name(default_role_name)
        if role:
            user.roles.append(role)

        await self.db.commit()
        await self.db.refresh(user)

        # Kick off email verification OTP asynchronously
        await self.request_otp(user, OTPPurpose.EMAIL_VERIFICATION)
        return user

    @staticmethod
    def _default_role_for_user_type(user_type: UserType) -> str:
        return {
            UserType.EMPLOYEE: "EMPLOYEE",
            UserType.EMPLOYER_ADMIN: "EMPLOYER_ADMIN",
            UserType.LENDER: "LENDER",
            UserType.PLATFORM_ADMIN: "PLATFORM_ADMIN",
            UserType.SUPPORT: "SUPPORT",
        }[user_type]

    async def authenticate(self, payload: UserLoginRequest) -> User:
        user = await self.user_repo.get_by_email(payload.email)
        if user is None:
            raise InvalidCredentialsException("Invalid email or password")

        if user.locked_until and user.locked_until > datetime.now(timezone.utc):
            raise ForbiddenException(f"Account locked until {user.locked_until.isoformat()} due to repeated failed logins")

        if not verify_password(payload.password, user.hashed_password):
            user.failed_login_attempts += 1
            if user.failed_login_attempts >= MAX_FAILED_LOGIN_ATTEMPTS:
                user.locked_until = datetime.now(timezone.utc) + timedelta(minutes=LOCKOUT_MINUTES)
            await self.db.commit()
            raise InvalidCredentialsException("Invalid email or password")

        if not user.is_active:
            raise ForbiddenException("Account is deactivated. Contact support.")

        user.failed_login_attempts = 0
        user.locked_until = None
        user.last_login_at = datetime.now(timezone.utc)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def issue_tokens(self, user: User, device_info: str | None = None, ip_address: str | None = None) -> dict:
        role_names = [r.name for r in user.roles]
        access_token = create_access_token(str(user.id), role_names, user.user_type.value)
        refresh_token = create_refresh_token(str(user.id))

        token_hash = hashlib.sha256(refresh_token.encode()).hexdigest()
        await self.refresh_repo.create(
            user_id=user.id,
            token_hash=token_hash,
            expires_at=datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
            device_info=device_info,
            ip_address=ip_address,
        )
        await self.db.commit()

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        }

    async def refresh_access_token(self, refresh_token: str) -> dict:
        payload = decode_refresh_token(refresh_token)
        token_hash = hashlib.sha256(refresh_token.encode()).hexdigest()
        stored = await self.refresh_repo.get_by_hash(token_hash)

        if stored is None or stored.revoked or stored.expires_at < datetime.now(timezone.utc):
            raise InvalidTokenException("Refresh token is invalid, expired, or revoked")

        user = await self.user_repo.get_by_id(uuid.UUID(payload["sub"]))
        if user is None or not user.is_active:
            raise InvalidTokenException("User is no longer active")

        # Rotate: revoke old, issue new
        stored.revoked = True
        await self.db.commit()
        return await self.issue_tokens(user)

    async def logout(self, user: User) -> None:
        await self.refresh_repo.revoke_all_for_user(user.id)
        await self.db.commit()

    # ---------------- OTP ----------------

    async def request_otp(self, user: User, purpose: OTPPurpose) -> None:
        code = generate_otp_code()
        await self.otp_repo.create(
            user_id=user.id,
            code_hash=hash_otp(code),
            purpose=purpose,
            expires_at=datetime.now(timezone.utc) + timedelta(minutes=settings.OTP_EXPIRE_MINUTES),
        )
        await self.db.commit()

        if purpose in (OTPPurpose.EMAIL_VERIFICATION, OTPPurpose.PASSWORD_RESET):
            send_email_task.delay(
                to_email=user.email,
                subject=f"Your SalaryFund AI verification code",
                body=f"Your one-time code is {code}. It expires in {settings.OTP_EXPIRE_MINUTES} minutes.",
            )
        else:
            send_sms_task.delay(
                to_phone=user.phone_number,
                message=f"Your SalaryFund AI OTP is {code}. Valid for {settings.OTP_EXPIRE_MINUTES} minutes.",
            )

    async def verify_otp(self, user_id: uuid.UUID, code: str, purpose: OTPPurpose) -> bool:
        otp = await self.otp_repo.get_latest_active(user_id, purpose)
        if otp is None:
            raise OTPException("No active OTP found. Please request a new code.")

        if otp.expires_at < datetime.now(timezone.utc):
            raise OTPException("OTP has expired. Please request a new code.")

        if otp.attempts >= MAX_OTP_ATTEMPTS:
            raise OTPException("Maximum OTP attempts exceeded. Please request a new code.")

        if not verify_otp(code, otp.code_hash):
            otp.attempts += 1
            await self.db.commit()
            raise OTPException("Incorrect OTP code.")

        otp.consumed = True
        user = await self.user_repo.get_by_id(user_id)

        if purpose == OTPPurpose.EMAIL_VERIFICATION:
            user.is_email_verified = True
        elif purpose == OTPPurpose.PHONE_VERIFICATION:
            user.is_phone_verified = True

        await self.db.commit()
        return True
