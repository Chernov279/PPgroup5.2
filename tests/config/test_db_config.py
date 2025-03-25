from pathlib import Path
from typing import Optional

from pydantic import ConfigDict
from pydantic_settings import BaseSettings

from src.config.database.db_helper import DatabaseHelper


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
        "env_file": str(Path(__file__).parent.parent.parent / ".env"),
        "extra": "ignore"
    }


test_settings = SettingsForTests()

test_db_helper = DatabaseHelper(url=test_settings.TEST_DATABASE_URL, echo=True)
