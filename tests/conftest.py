import logging
from pathlib import Path
from typing import Optional

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from pydantic_settings import BaseSettings
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.database.db_helper import DatabaseHelper, get_db_session
from src.main import app

logger = logging.getLogger(__name__)


class SettingsForTests(BaseSettings):
    TEST_DATABASE_NAME: str
    TEST_DATABASE_HOST: str
    TEST_DATABASE_USERNAME: str
    TEST_DATABASE_PASSWORD: str
    TEST_DATABASE_PORT: int

    TEST_DATABASE_URL: Optional[str] = None
    TEST_DATABASE_URL_SYNC: Optional[str] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.TEST_DATABASE_URL:
            self.TEST_DATABASE_URL = (
                f"postgresql+asyncpg://{self.TEST_DATABASE_USERNAME}:{self.TEST_DATABASE_PASSWORD}"
                f"@{self.TEST_DATABASE_HOST}:{self.TEST_DATABASE_PORT}/{self.TEST_DATABASE_NAME}"
            )
        if not self.TEST_DATABASE_URL_SYNC:
            self.TEST_DATABASE_URL_SYNC = (
                f"postgresql+psycopg2://{self.TEST_DATABASE_USERNAME}:{self.TEST_DATABASE_PASSWORD}"
                f"@{self.TEST_DATABASE_HOST}:{self.TEST_DATABASE_PORT}/{self.TEST_DATABASE_NAME}"
            )

    model_config = {
        "env_file": str(Path(__file__).parent.parent / ".env"),
        "extra": "ignore"
    }

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