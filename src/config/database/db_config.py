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

    DATABASE_URL: Optional[str] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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

        self.DATABASE_URL = f"postgresql://{self.DATABASE_USERNAME}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"

    # получение данных из файла .env
    class Config:
        env_file = str(Path(__file__).parent.parent.parent.parent / ".env")
        extra = "ignore"


try:
    settings_db = ConfigDataBase()
    # os.environ["DATABASE_URL"] = settings.database_url
except ValidationError as e:
    print("Ошибка валидации Pydantic:", e)
except ValueError as e:
    print("Ошибка инициализации настроек:", e)