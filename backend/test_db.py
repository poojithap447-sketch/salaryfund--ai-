"""
Standalone database connection tester script for SalaryFund AI backend.
Executes 'SELECT 1' against the configured PostgreSQL database.
Does NOT print or log passwords, secrets, or sensitive credentials.
"""
import asyncio
import sys
from sqlalchemy import text

from app.database.session import AsyncSessionLocal
from app.core.config import settings


async def test_connection():
    # Mask password for display
    url_parts = settings.DATABASE_URL.split("@")
    host_info = url_parts[-1] if len(url_parts) > 1 else "configured host"
    print(f"[*] Testing database connection to target: {host_info} ...")

    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(text("SELECT 1"))
            val = result.scalar()
            if val == 1:
                print("[SUCCESS] Database connection verified! 'SELECT 1' returned 1.")
                return True
            else:
                print(f"[UNEXPECTED] Query returned: {val}")
                return False
    except Exception as exc:
        error_type = type(exc).__name__
        raw_msg = str(exc).splitlines()[0] if str(exc) else ""
        print(f"[FAILED] Database connection failed: {error_type} - {raw_msg}")
        return False


if __name__ == "__main__":
    success = asyncio.run(test_connection())
    sys.exit(0 if success else 1)
