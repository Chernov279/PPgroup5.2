import pytest

PATH = "/auth/register"

@pytest.mark.asyncio
async def test_register_success(client):
    payload = {
        "email": "test@example.com",
        "password": "Password123!",
        "name": "Test",
    }

    response = await client.post(PATH, json=payload)

    assert response.status_code == 201
    data = response.json()

    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "Bearer"

    assert data["access_token"]
    assert data["refresh_token"]