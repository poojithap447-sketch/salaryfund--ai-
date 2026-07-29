"""
Reusable FastAPI dependencies for authentication and role-based access control.
"""
import uuid
from typing import Annotated

from fastapi import Depends, Header
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ForbiddenException, InvalidTokenException, UnauthorizedException
from app.database.session import get_db_session
from app.models.rbac import User
from app.security.jwt_handler import decode_access_token

bearer_scheme = HTTPBearer(auto_error=False)

DBSession = Annotated[AsyncSession, Depends(get_db_session)]


async def get_current_user(
    db: DBSession,
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)] = None,
) -> User:
    if credentials is None:
        raise UnauthorizedException("Missing bearer token")

    payload = decode_access_token(credentials.credentials)
    user_id = payload.get("sub")
    if not user_id:
        raise InvalidTokenException("Token missing subject claim")

    result = await db.execute(select(User).where(User.id == uuid.UUID(user_id)))
    user = result.scalar_one_or_none()
    if user is None:
        raise UnauthorizedException("User not found")
    if not user.is_active:
        raise ForbiddenException("User account is deactivated")
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def require_roles(*allowed_roles: str):
    """Dependency factory enforcing RBAC: user must hold at least one of allowed_roles."""

    async def _checker(current_user: CurrentUser) -> User:
        user_role_names = {role.name for role in current_user.roles}
        if not user_role_names.intersection(allowed_roles):
            raise ForbiddenException(
                f"Requires one of roles: {', '.join(allowed_roles)}",
            )
        return current_user

    return _checker


def require_permissions(*required_permissions: str):
    """Dependency factory enforcing fine-grained permission codes, e.g. 'loans:approve'."""

    async def _checker(current_user: CurrentUser) -> User:
        granted = {perm.code for role in current_user.roles for perm in role.permissions}
        if not set(required_permissions).issubset(granted):
            raise ForbiddenException(
                f"Missing required permissions: {', '.join(set(required_permissions) - granted)}",
            )
        return current_user

    return _checker


async def get_client_ip(x_forwarded_for: Annotated[str | None, Header()] = None) -> str | None:
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    return None
