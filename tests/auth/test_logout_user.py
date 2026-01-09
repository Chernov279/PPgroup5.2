import pytest
from httpx import AsyncClient

from tests.auth.constants import REGISTER_PATH, VALID_REGISTER_USER, REFRESH_TOKEN_SCHEMA, LOGOUT_PATH, LOGIN_PATH, \
    VALID_LOGIN_USER, REFRESH_PATH


@pytest.mark.asyncio
async def test_logout_success(client: AsyncClient):
    """Проверяет успешный выход из текущей сессии"""

    register_response = await client.post(REGISTER_PATH, json=VALID_REGISTER_USER)
    refresh_token = register_response.json()["refresh_token"]

    json = REFRESH_TOKEN_SCHEMA.copy()
    json["refresh_token"] = refresh_token
    response = await client.post(LOGOUT_PATH, json=json)

    assert response.status_code == 200
    data = response.json()
    assert "successfully logged out" in data["message"].lower()


@pytest.mark.asyncio
async def test_logout_revoke_token(client: AsyncClient):
    """Проверяет отказ при повторном входе после logout"""

    register_response = await client.post(REGISTER_PATH, json=VALID_REGISTER_USER)
    refresh_token = register_response.json()["refresh_token"]

    json = REFRESH_TOKEN_SCHEMA.copy()
    json["refresh_token"] = refresh_token
    await client.post(LOGOUT_PATH, json=json)

    response = await client.post(REFRESH_PATH, json=json)

    assert response.status_code == 403
    data = response.json()
    assert "revoked" in str(data).lower()


@pytest.mark.asyncio
async def test_logout_other_session(client: AsyncClient):
    """Проверяет возможность входа после logout для другой сессии"""

    register_response = await client.post(REGISTER_PATH, json=VALID_REGISTER_USER)
    refresh_token = register_response.json()["refresh_token"]

    json = REFRESH_TOKEN_SCHEMA.copy()
    json["refresh_token"] = refresh_token

    other_login_response = await client.post(LOGIN_PATH, json=VALID_LOGIN_USER)
    other_refresh_token = other_login_response.json()["refresh_token"]

    other_json = REFRESH_TOKEN_SCHEMA.copy()
    other_json["refresh_token"] = other_refresh_token

    await client.post(LOGOUT_PATH, json=json)
    response = await client.post(REFRESH_PATH, json=other_json)

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["refresh_token"] != refresh_token