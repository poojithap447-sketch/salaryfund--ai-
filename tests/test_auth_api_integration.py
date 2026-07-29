"""
Integration tests for the authentication API, run against a real (test) Postgres
database via the db_session fixture in conftest.py, which creates/drops all
tables around each test for isolation.
"""
import uuid

TEST_EMAIL = f"testuser_{uuid.uuid4().hex[:8]}@example.com"
WRONGPASS_EMAIL = f"wrongpass_{uuid.uuid4().hex[:8]}@example.com"
DUPE_EMAIL = f"dupe_{uuid.uuid4().hex[:8]}@example.com"

import pytest

pytestmark = pytest.mark.asyncio


async def test_health_check(client):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] in ("ok", "degraded")


async def test_register_and_login_flow(client, db_session):
    register_resp = await client.post(
        "/api/v1/auth/register",
        json={
            "email": TEST_EMAIL,
            "phone_number": "+919000000001",
            "password": "TestPass1!",
            "user_type": "EMPLOYEE",
        },
    )
    assert register_resp.status_code == 201
    body = register_resp.json()
    assert body["email"] == TEST_EMAIL
    assert body["is_active"] is True

    login_resp = await client.post(
        "/api/v1/auth/login",
        json={"email": TEST_EMAIL, "password": "TestPass1!"},
    )
    assert login_resp.status_code == 200
    tokens = login_resp.json()
    assert "access_token" in tokens
    assert "refresh_token" in tokens

    me_resp = await client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {tokens['access_token']}"})
    assert me_resp.status_code == 200
    assert me_resp.json()["email"] == TEST_EMAIL


async def test_login_with_wrong_password_fails(client, db_session):
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": WRONGPASS_EMAIL,
            "phone_number": "+919000000002",
            "password": "TestPass1!",
            "user_type": "EMPLOYEE",
        },
    )
    login_resp = await client.post(
        "/api/v1/auth/login",
        json={"email": WRONGPASS_EMAIL, "password": "IncorrectPassword!"},
    )
    assert login_resp.status_code == 401


async def test_duplicate_registration_rejected(client, db_session):
    payload = {
        "email": DUPE_EMAIL,
        "phone_number": "+919000000003",
        "password": "TestPass1!",
        "user_type": "EMPLOYEE",
    }
    first = await client.post("/api/v1/auth/register", json=payload)
    assert first.status_code == 201
    second = await client.post("/api/v1/auth/register", json=payload)
    assert second.status_code == 409


async def test_unauthenticated_request_rejected(client):
    response = await client.get("/api/v1/auth/me")
    assert response.status_code == 401
