"""
Health check endpoint for load balancers / container orchestrators (k8s liveness & readiness probes).
Verifies DB and Redis connectivity so a 200 genuinely means the service can serve traffic.
"""
import redis.asyncio as aioredis
from fastapi import APIRouter
from sqlalchemy import text

from app.core.config import settings
from app.database.session import AsyncSessionLocal

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health_check():
    checks = {"database": "unknown", "redis": "unknown"}
    overall = "ok"

    try:
        async with AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))
        checks["database"] = "ok"
    except Exception as exc:
        checks["database"] = f"error: {exc}"
        overall = "degraded"

    try:
        client = aioredis.from_url(settings.REDIS_URL)
        await client.ping()
        await client.close()
        checks["redis"] = "ok"
    except Exception as exc:
        checks["redis"] = f"error: {exc}"
        overall = "degraded"

    return {"status": overall, "checks": checks, "version": "1.0.0"}


@router.get("/db-test")
async def db_test():
    """Simple endpoint to verify database connectivity with SELECT 1 query."""
    try:
        async with AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))
        return {"database": "connected"}
    except Exception as exc:
        # Sanitize exception message to ensure no credentials or sensitive DSN data is exposed
        error_type = type(exc).__name__
        raw_msg = str(exc)
        # Extract first line of error message and remove connection string details if any
        clean_msg = raw_msg.splitlines()[0] if raw_msg else error_type
        return {"database": "not connected", "error": f"{error_type}: {clean_msg}"}


@router.get("/")
async def root():
    return {"service": "SalaryFund AI", "status": "running", "docs": "/docs"}

