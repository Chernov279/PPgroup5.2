import pytest
from httpx import AsyncClient

from tests.auth.constants import REGISTER_PATH, VALID_REGISTER_USER, SAME_EMAIL_VALID_REGISTER_USER, INVALID_EMAIL_REGISTER_USER, \
    WEAK_PASSWORD_REGISTER_USER, OPTIONAL_FIELDS_VALID_REGISTER_USER


@pytest.mark.asyncio
async def test_register_success(client: AsyncClient):
    """Проверяет успешную регистрацию нового пользователя"""
    payload = VALID_REGISTER_USER

    response = await client.post(REGISTER_PATH, json=payload)

    assert response.status_code == 201
    data = response.json()

    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "Bearer"
    assert len(data["access_token"]) > 50  # JWT должен быть достаточно длинным
    assert len(data["refresh_token"]) > 50


@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient):
    """Проверяет, что нельзя зарегистрироваться с существующим email"""
    payload1 = VALID_REGISTER_USER
    await client.post(REGISTER_PATH, json=payload1)

    payload2 = SAME_EMAIL_VALID_REGISTER_USER

    response = await client.post(REGISTER_PATH, json=payload2)

    assert response.status_code == 409
    assert "email" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_register_invalid_email_format(client: AsyncClient):
    """Проверяет валидацию формата email"""
    payload = INVALID_EMAIL_REGISTER_USER

    response = await client.post(REGISTER_PATH, json=payload)

    assert response.status_code == 400
    data = response.json()
    assert "email" in str(data).lower() or "validation" in str(data).lower()


@pytest.mark.asyncio
async def test_register_weak_password(client: AsyncClient):
    """Проверяет валидацию сложности пароля"""
    payload = WEAK_PASSWORD_REGISTER_USER

    response = await client.post(REGISTER_PATH, json=payload)

    assert response.status_code == 400
    data = response.json()
    assert "password" in str(data).lower()


@pytest.mark.asyncio
async def test_register_with_optional_fields(client: AsyncClient):
    """Проверяет регистрацию с опциональными полями"""
    payload = OPTIONAL_FIELDS_VALID_REGISTER_USER

    response = await client.post(REGISTER_PATH, json=payload)

    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
