import pytest
from httpx import AsyncClient

from tests.auth.constants import VALID_REGISTER_USER, REGISTER_PATH, VALID_LOGIN_USER, LOGIN_PATH, \
    WRONG_PASSWORD_LOGIN_USER


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient):
    """Проверяет успешный логин с правильными учетными данными"""

    register_payload = VALID_REGISTER_USER
    await client.post(REGISTER_PATH, json=register_payload)

    login_payload = VALID_LOGIN_USER

    response = await client.post(LOGIN_PATH, json=login_payload)

    assert response.status_code == 200
    data = response.json()

    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "Bearer"


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient):
    """Проверяет логин с неверным паролем"""

    register_payload = VALID_REGISTER_USER
    await client.post(LOGIN_PATH, json=register_payload)

    login_payload = WRONG_PASSWORD_LOGIN_USER

    response = await client.post(LOGIN_PATH, json=login_payload)

    assert response.status_code == 401
    assert "password" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_login_nonexistent_user(client: AsyncClient):
    """Проверяет логин несуществующего пользователя"""
    login_payload = WRONG_PASSWORD_LOGIN_USER

    response = await client.post(LOGIN_PATH, json=login_payload)

    assert response.status_code == 401
    assert "email" in response.json()["detail"].lower() or "not found" in response.json()["detail"].lower()

