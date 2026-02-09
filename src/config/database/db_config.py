from typing import Optional

from pydantic import ValidationError, ConfigDict
from pydantic_settings import BaseSettings
from pathlib import Path


class ConfigDataBase(BaseSettings):
    """
    Конфигурация подключения к базе данных.

    """

    POSTGRES_DB: str | None = None
    POSTGRES_HOST: str = "localhost"
    POSTGRES_USER: str | None = None
    POSTGRES_PASSWORD: str | None = None
    POSTGRES_PORT: str = "5432"

    POSTGRES_ECHO_LOG: bool = True

    POSTGRES_URL: str | None = None
    POSTGRES_URL_SYNC: str | None = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if not self.POSTGRES_URL_SYNC:
            self._build_sync_url()

        if not self.POSTGRES_URL:
            self._build_async_url()

    def _build_async_url(self) -> None:
        self._validate_credentials()

        self.POSTGRES_URL = (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    def _build_sync_url(self) -> None:
        self._validate_credentials()

        self.POSTGRES_URL_SYNC = (
            f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    def _validate_credentials(self) -> None:
        missing = [
            name for name in (
                "POSTGRES_DB",
                "POSTGRES_USER",
                "POSTGRES_PASSWORD",
            )
            if not getattr(self, name)
        ]
        if missing:
            raise ValueError(
                f"Не заданы обязательные параметры БД: {', '.join(missing)}"
            )


try:
    settings_db = ConfigDataBase()
except ValidationError as e:
    print("Ошибка валидации Pydantic:", e)
except ValueError as e:
    print("Ошибка инициализации настроек:", e)
