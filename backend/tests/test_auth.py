import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_auth_login_success(client: AsyncClient, seed_users):
    """Test valid user authentication returns JWT access and refresh tokens."""
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": "admin@test.com", "password": "AdminPass123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["role"] == "ADMIN"
    assert data["email"] == "admin@test.com"


@pytest.mark.asyncio
async def test_auth_login_invalid_password(client: AsyncClient, seed_users):
    """Test login failure with invalid password."""
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": "admin@test.com", "password": "WrongPassword!"}
    )
    assert response.status_code == 401
    assert "Invalid email or password" in response.json()["detail"]


@pytest.mark.asyncio
async def test_auth_rbac_endpoint_protection(client: AsyncClient, auth_headers):
    """Test that unauthorized roles are forbidden from accessing admin endpoints."""
    # Patient attempting to access admin user list
    patient_headers = auth_headers("patient")
    response = await client.get("/api/v1/users", headers=patient_headers)
    assert response.status_code == 403

    # Admin accessing same endpoint
    admin_headers = auth_headers("admin")
    response = await client.get("/api/v1/users", headers=admin_headers)
    assert response.status_code == 200
