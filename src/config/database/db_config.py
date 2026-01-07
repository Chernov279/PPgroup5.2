from typing import Optional

from pydantic import ValidationError, ConfigDict
from pydantic_settings import BaseSettings
from pathlib import Path


class ConfigDataBase(BaseSettings):
    """
    Конфигурация подключения к базе данных.

    """

    DATABASE_NAME: str | None = None
    DATABASE_HOST: str = "localhost"
    DATABASE_USERNAME: str | None = None
    DATABASE_PASSWORD: str | None = None
    DATABASE_PORT: str = "5432"

    DB_ECHO_LOG: bool = True

    DATABASE_URL: str | None = None
    DATABASE_URL_SYNC: str | None = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if not self.DATABASE_URL_SYNC:
            self._build_sync_url()

        if not self.DATABASE_URL:
            self._build_async_url()

    def _build_async_url(self) -> None:
        self._validate_credentials()

        self.DATABASE_URL = (
            f"postgresql+asyncpg://{self.DATABASE_USERNAME}:{self.DATABASE_PASSWORD}"
            f"@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
        )

    def _build_sync_url(self) -> None:
        self._validate_credentials()

        self.DATABASE_URL_SYNC = (
            f"postgresql+psycopg2://{self.DATABASE_USERNAME}:{self.DATABASE_PASSWORD}"
            f"@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
        )

    def _validate_credentials(self) -> None:
        missing = [
            name for name in (
                "DATABASE_NAME",
                "DATABASE_USERNAME",
                "DATABASE_PASSWORD",
            )
            if not getattr(self, name)
        ]
        if missing:
            raise ValueError(
                f"Не заданы обязательные параметры БД: {', '.join(missing)}"
            )

    model_config = {
        "env_file": str(Path(__file__).parent.parent.parent.parent / ".env"),
        "extra": "ignore",
    }


try:
    settings_db = ConfigDataBase()
except ValidationError as e:
    print("Ошибка валидации Pydantic:", e)
except ValueError as e:
    print("Ошибка инициализации настроек:", e)
