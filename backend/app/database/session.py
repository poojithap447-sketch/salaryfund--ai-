"""
Async SQLAlchemy engine/session factory.
Uses asyncpg driver. A single engine is shared across the app lifetime.
"""
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings

connect_args = {}
if "neon.tech" in settings.DATABASE_URL:
    try:
        host_part = settings.DATABASE_URL.split("@")[-1].split("/")[0]
        endpoint_id = host_part.split(".")[0].replace("-pooler", "")
        connect_args["server_settings"] = {"options": f"endpoint={endpoint_id}"}
    except Exception:
        pass

engine = create_async_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_pre_ping=True,
    echo=settings.DEBUG,
    future=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


async def get_db_session() -> AsyncSession:
    """Yields a scoped AsyncSession, ensuring rollback on error and closure after use."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
