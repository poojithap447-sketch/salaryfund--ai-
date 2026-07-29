"""
Authentication flow tests: registration, duplicate-email rejection, weak
password rejection, login success/failure, and JWT-protected /auth/me.
"""
import pytest


async def test_register_and_login(client, unique_suffix):
    email = f"testuser_{unique_suffix}@example.com"
    password = "TestPass123!"

    register_resp = await client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "phone_number": f"+9198765{unique_suffix[:5]}",
            "password": password,
            "user_type": "EMPLOYEE",
        },
    )
    assert register_resp.status_code == 201
    body = register_resp.json()
    assert body["email"] == email
    assert body["is_active"] is True

    login_resp = await client.post("/api/v1/auth/login", json={"email": email, "password": password})
    assert login_resp.status_code == 200
    tokens = login_resp.json()
    assert "access_token" in tokens
    assert "refresh_token" in tokens

    me_resp = await client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {tokens['access_token']}"})
    assert me_resp.status_code == 200
    assert me_resp.json()["email"] == email


async def test_register_weak_password_rejected(client, unique_suffix):
    resp = await client.post(
        "/api/v1/auth/register",
        json={
            "email": f"weak_{unique_suffix}@example.com",
            "phone_number": f"+9198764{unique_suffix[:5]}",
            "password": "weakpass",  # no uppercase, no digit, no special char
            "user_type": "EMPLOYEE",
        },
    )
    assert resp.status_code == 422


async def test_duplicate_registration_rejected(client, unique_suffix):
    email = f"dup_{unique_suffix}@example.com"
    payload = {
        "email": email,
        "phone_number": f"+9198763{unique_suffix[:5]}",
        "password": "TestPass123!",
        "user_type": "EMPLOYEE",
    }
    first = await client.post("/api/v1/auth/register", json=payload)
    assert first.status_code == 201

    second = await client.post("/api/v1/auth/register", json=payload)
    assert second.status_code == 409
    assert second.json()["error_code"] == "ALREADY_EXISTS"


async def test_login_wrong_password_rejected(client, unique_suffix):
    email = f"wrongpass_{unique_suffix}@example.com"
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "phone_number": f"+9198762{unique_suffix[:5]}",
            "password": "TestPass123!",
            "user_type": "EMPLOYEE",
        },
    )
    resp = await client.post("/api/v1/auth/login", json={"email": email, "password": "WrongPassword!"})
    assert resp.status_code == 401
    assert resp.json()["error_code"] == "INVALID_CREDENTIALS"


async def test_protected_route_requires_token(client):
    resp = await client.get("/api/v1/auth/me")
    assert resp.status_code == 401
