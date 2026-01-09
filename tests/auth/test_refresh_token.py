import pytest
from httpx import AsyncClient

from tests.auth.constants import REGISTER_PATH, VALID_REGISTER_USER, REFRESH_PATH, INVALID_REFRESH_USER, \
    REFRESH_TOKEN_SCHEMA, REFRESH_TOKEN_KEY


@pytest.mark.asyncio
async def test_refresh_token_success(client: AsyncClient):
    """Проверяет успешное обновление access токена"""

    register_response = await client.post(REGISTER_PATH, json=VALID_REGISTER_USER)
    refresh_token = register_response.json()["refresh_token"]

    refresh_payload = {"refresh_token": refresh_token}

    response = await client.post(REFRESH_PATH, json=refresh_payload)

    assert response.status_code == 200
    data = response.json()

    assert "access_token" in data
    assert "refresh_token" in data
    assert data["refresh_token"] != refresh_token


@pytest.mark.asyncio
async def test_refresh_token_invalid(client: AsyncClient):
    """Проверяет обновление с невалидным refresh токеном"""

    response = await client.post(REFRESH_PATH, json=INVALID_REFRESH_USER)

    assert response.status_code == 401
    assert "invalid" in response.json()["detail"].lower() or "token" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_refresh_token_with_cookie(client: AsyncClient):
    """Проверяет обновление токена с refresh токеном в cookie"""

    register_response = await client.post(REGISTER_PATH, json=VALID_REGISTER_USER)
    refresh_token = register_response.json()["refresh_token"]

    cookies = REFRESH_TOKEN_SCHEMA.copy()
    cookies[REFRESH_TOKEN_KEY] = refresh_token

    response = await client.post(REFRESH_PATH, cookies=cookies)

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data