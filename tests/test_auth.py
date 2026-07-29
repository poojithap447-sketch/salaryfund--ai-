"""Integration tests for the authentication flow."""
import uuid

import pytest


@pytest.mark.asyncio
async def test_register_and_login(client):
    email = f"test_{uuid.uuid4().hex[:8]}@example.com"
    register_resp = await client.post(
        "/api/v1/auth/register",
        json={"email": email, "phone_number": "+919812345678", "password": "TestPass1!", "user_type": "EMPLOYEE"},
    )
    assert register_resp.status_code == 201
    body = register_resp.json()
    assert body["email"] == email
    assert body["is_active"] is True

    login_resp = await client.post("/api/v1/auth/login", json={"email": email, "password": "TestPass1!"})
    assert login_resp.status_code == 200
    tokens = login_resp.json()
    assert "access_token" in tokens
    assert "refresh_token" in tokens
    assert tokens["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_with_wrong_password_fails(client):
    email = f"test_{uuid.uuid4().hex[:8]}@example.com"
    await client.post(
        "/api/v1/auth/register",
        json={"email": email, "phone_number": "+919812345679", "password": "TestPass1!", "user_type": "EMPLOYEE"},
    )
    resp = await client.post("/api/v1/auth/login", json={"email": email, "password": "WrongPassword!"})
    assert resp.status_code == 401
    assert resp.json()["error_code"] == "INVALID_CREDENTIALS"


@pytest.mark.asyncio
async def test_weak_password_rejected(client):
    resp = await client.post(
        "/api/v1/auth/register",
        json={"email": "weakpass@example.com", "phone_number": "+919812345680", "password": "weak", "user_type": "EMPLOYEE"},
    )
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_get_me_requires_auth(client):
    resp = await client.get("/api/v1/auth/me")
    assert resp.status_code == 401
