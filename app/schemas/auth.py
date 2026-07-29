import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.models.rbac import OTPPurpose, UserType


class UserRegisterRequest(BaseModel):
    email: EmailStr
    phone_number: str = Field(..., min_length=8, max_length=20)
    password: str = Field(..., min_length=8, max_length=128)
    user_type: UserType

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        if not any(not c.isalnum() for c in v):
            raise ValueError("Password must contain at least one special character")
        return v


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


class OTPRequestSchema(BaseModel):
    phone_number: str | None = None
    email: EmailStr | None = None
    purpose: OTPPurpose


class OTPVerifyRequest(BaseModel):
    user_id: uuid.UUID
    code: str = Field(..., min_length=4, max_length=8)
    purpose: OTPPurpose


class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8, max_length=128)


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    email: EmailStr
    phone_number: str
    user_type: UserType
    is_active: bool
    is_email_verified: bool
    is_phone_verified: bool
    mfa_enabled: bool
    last_login_at: datetime | None
    created_at: datetime


class MFAEnableResponse(BaseModel):
    secret: str
    provisioning_uri: str
