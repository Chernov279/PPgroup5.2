from typing import Optional

from pydantic import ValidationError
from pydantic_settings import BaseSettings
from pathlib import Path


class ConfigDataBase(BaseSettings):
    # получение чувствительных данных из корневой папки
    # ПРИ ОБНОВЛЕНИИ ДАННЫХ БД ПЕРЕЗАПУСТИТЬ, ЧТОБЫ ОБНОВИТЬ URL!!!

    DATABASE_NAME: str = None
    DATABASE_HOST: str = "localhost"
    DATABASE_USERNAME: str = None
    DATABASE_PASSWORD: str = None
    DATABASE_PORT: str = "5432"

    DB_ECHO_LOG: bool = True
    DATABASE_URL: Optional[str] = None
    DATABASE_URL_SYNC: Optional[str] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if self.DATABASE_URL:
            return

        missing_fields = [
            field for field in [
                "DATABASE_NAME",
                "DATABASE_PASSWORD",
                "DATABASE_USERNAME",
            ]
            if not getattr(self, field, None)
        ]
        if missing_fields:
            raise ValueError(f"Следующие параметры не переданы или пустые: {', '.join(missing_fields)}")

        self.DATABASE_URL = (
            f"postgresql+asyncpg://{self.DATABASE_USERNAME}:{self.DATABASE_PASSWORD}"
            f"@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
        )
        self.DATABASE_URL_SYNC = (
            f"postgresql+psycopg2://{self.DATABASE_USERNAME}:{self.DATABASE_PASSWORD}"
            f"@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
        )

    # получение данных из файла .env
    class Config:
        env_file = str(Path(__file__).parent.parent.parent.parent / ".env")
        extra = "ignore"


try:
    settings_db = ConfigDataBase()
except ValidationError as e:
    print("Ошибка валидации Pydantic:", e)
except ValueError as e:
    print("Ошибка инициализации настроек:", e)
