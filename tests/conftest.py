import logging
import uuid
from pathlib import Path
from typing import Optional, Any, AsyncGenerator

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from pydantic_settings import BaseSettings
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.database.db_helper import DatabaseHelper, get_db_session
from src.main import app
from tests.auth.constants import REGISTER_PATH, LOGIN_PATH

logger = logging.getLogger(__name__)


class SettingsForTests(BaseSettings):
    TEST_POSTGRES_DB: str
    TEST_POSTGRES_HOST: str
    TEST_POSTGRES_USER: str
    TEST_POSTGRES_PASSWORD: str
    TEST_POSTGRES_PORT: int

    TEST_POSTGRES_URL: Optional[str] = None
    TEST_POSTGRES_URL_SYNC: Optional[str] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.TEST_POSTGRES_URL:
            self.TEST_POSTGRES_URL = (
                f"postgresql+asyncpg://{self.TEST_POSTGRES_USER}:{self.TEST_POSTGRES_PASSWORD}"
                f"@{self.TEST_POSTGRES_HOST}:{self.TEST_POSTGRES_PORT}/{self.TEST_POSTGRES_DB}"
            )
        if not self.TEST_POSTGRES_URL_SYNC:
            self.TEST_POSTGRES_URL_SYNC = (
                f"postgresql+psycopg2://{self.TEST_POSTGRES_USER}:{self.TEST_POSTGRES_PASSWORD}"
                f"@{self.TEST_POSTGRES_HOST}:{self.TEST_POSTGRES_PORT}/{self.TEST_POSTGRES_DB}"
            )

test_settings = SettingsForTests()
test_db_helper = DatabaseHelper(url=test_settings.TEST_DATABASE_URL, echo=True)



@pytest_asyncio.fixture
async def engine():
    """Движок базы данных для тестов."""
    engine = test_db_helper.engine

    yield engine

    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def db_session(engine):
    """Изолированная сессия для каждого теста."""
    connection = await engine.connect()
    transaction = await connection.begin()

    session = AsyncSession(
        bind=connection,
        expire_on_commit=False,
    )

    yield session

    await session.close()
    await transaction.rollback()
    await connection.close()


@pytest_asyncio.fixture(scope="function")
async def client(db_session):
    """Клиент FastAPI."""

    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db_session] = override_get_db

    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
            timeout=30.0
    ) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def debug_response():
    """Фикстура для отладки ответов."""

    def _debug(response, expected_status=None):
        logger.warning(f"URL: {response.url}")
        logger.warning(f"Status Code: {response.status_code}")
        logger.warning(f"Headers: {dict(response.headers)}")
        logger.warning(f"Response Body: {response.text[:500]}")  # Первые 500 символов

        if expected_status and response.status_code != expected_status:
            logger.error(f"Expected {expected_status}, got {response.status_code}")
            logger.error(f"Full response: {response.text}")

    return _debug


@pytest_asyncio.fixture(scope="function")
async def create_user(client: AsyncClient) -> AsyncGenerator:
    """Фабрика для создания тестовых пользователей"""

    created_users = []

    async def factory(**overrides) -> dict[str, Any]:
        """Создает пользователя с уникальными данными"""
        test_id = uuid.uuid4().hex[:8]

        user_data = {
            "name": f"User_{test_id}",
            "email": f"user_{test_id}@example.com",
            "password": "TestPass123!",
            **overrides
        }

        # Регистрация
        register_response = await client.post(REGISTER_PATH, json=user_data)
        assert 200 <= register_response.status_code <= 299 , f"Registration failed: {register_response.text}"

        # Логин для получения токена
        login_response = await client.post(LOGIN_PATH, json={
            "email": user_data["email"],
            "password": user_data["password"]
        })
        assert 200 <= login_response.status_code <= 299, f"Login failed: {login_response.text}"

        tokens = login_response.json()

        user_info = {
            "id": register_response.json().get("user_id"),
            "email": user_data["email"],
            "name": user_data["name"],
            "headers": {"Authorization": f"Bearer {tokens['access_token']}"},
            "access_token": tokens["access_token"],
            "refresh_token": tokens["refresh_token"],
            "raw_data": user_data
        }

        created_users.append(user_info)
        return user_info

    yield factory