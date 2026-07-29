"""
Pytest fixtures: async HTTP client bound to the FastAPI app. Tests run against
a real Postgres/Redis (see .env) rather than mocks, since ORM/constraint
behavior and AI-model file I/O are core things this suite needs to verify.
Each test uses unique emails/codes (via the `unique_suffix` fixture) so tests
can run repeatedly against a persistent dev database without collisions.
"""
import uuid

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def unique_suffix():
    return uuid.uuid4().hex[:8]
