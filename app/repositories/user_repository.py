import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.rbac import OTP, RefreshToken, Role, User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, User)

    async def get_by_email(self, email: str) -> User | None:
        result = await self.db.execute(select(User).where(User.email == email.lower()))
        return result.scalar_one_or_none()

    async def get_by_phone(self, phone_number: str) -> User | None:
        result = await self.db.execute(select(User).where(User.phone_number == phone_number))
        return result.scalar_one_or_none()

    async def get_role_by_name(self, name: str) -> Role | None:
        result = await self.db.execute(select(Role).where(Role.name == name))
        return result.scalar_one_or_none()


class RefreshTokenRepository(BaseRepository[RefreshToken]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, RefreshToken)

    async def get_by_hash(self, token_hash: str) -> RefreshToken | None:
        result = await self.db.execute(select(RefreshToken).where(RefreshToken.token_hash == token_hash))
        return result.scalar_one_or_none()

    async def revoke_all_for_user(self, user_id: uuid.UUID) -> None:
        result = await self.db.execute(select(RefreshToken).where(RefreshToken.user_id == user_id, RefreshToken.revoked.is_(False)))
        for token in result.scalars().all():
            token.revoked = True
        await self.db.flush()


class OTPRepository(BaseRepository[OTP]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, OTP)

    async def get_latest_active(self, user_id: uuid.UUID, purpose) -> OTP | None:
        result = await self.db.execute(
            select(OTP)
            .where(OTP.user_id == user_id, OTP.purpose == purpose, OTP.consumed.is_(False))
            .order_by(OTP.created_at.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()
