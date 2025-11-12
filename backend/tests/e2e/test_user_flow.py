import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_user_flow(client: AsyncClient) -> None:
    # Registration
    response = await client.post(
        "/api/v1/users/auth/register",
        json={
            "email": "test12@example.com",
            "password": "password123SDf.",
            "first_name": "Alex",
            "second_name": "John",
        },
    )
    assert response.status_code == status.HTTP_200_OK
    register_data = response.json()
    assert "id" in register_data
    assert "access_token" in register_data

    access_token = register_data["access_token"]

    # Login
    response = await client.post(
        "/api/v1/users/auth/login",
        json={"email": "test12@example.com", "password": "password123SDf."},
    )
    assert response.status_code == status.HTTP_200_OK
    login_data = response.json()
    assert "access_token" in login_data

    # Profile
    response = await client.get(
        "/api/v1/users/profile",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == status.HTTP_200_OK
    profile_data = response.json()
    assert profile_data["email"] == "test12@example.com"
