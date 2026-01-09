import pytest
from httpx import AsyncClient

from tests.auth.constants import VALID_REGISTER_USER, REGISTER_PATH, VALID_LOGIN_USER, \
    VALID_LOGIN_OATH2_USER

OAUTH2_PATH = "/auth/oauth2"


@pytest.mark.asyncio
async def test_oauth2_login_success(client: AsyncClient):
    """Проверяет успешный OAuth2-совместимый логин"""

    register_payload = VALID_REGISTER_USER
    await client.post(REGISTER_PATH, json=register_payload)

    form_data = VALID_LOGIN_OATH2_USER

    response = await client.post(OAUTH2_PATH, data=form_data)

    assert response.status_code == 200
    data = response.json()

    assert "access_token" in data
    assert "refresh_token" in data
    assert data.get("token_type", "").lower() == "bearer"


@pytest.mark.asyncio
async def test_oauth2_login_failure(client: AsyncClient, debug_response):
    """Проверяет неудачный OAuth2 логин — неверные учетные данные"""

    form_data = VALID_LOGIN_OATH2_USER

    response = await client.post(OAUTH2_PATH, data=form_data)
    debug_response(response)
    assert response.status_code == 401
    assert "password" in response.json()["detail"].lower()