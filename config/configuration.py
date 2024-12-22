from typing import Optional, List, Union

from pydantic import ValidationError
from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    # получение чувствительных данных из корневой папки
    # ПРИ ОБНОВЛЕНИИ ДАННЫХ БД ПЕРЕЗАПУСТИТЬ, ЧТОБЫ ОБНОВИТЬ URL!!!

    project_name: str = None
    debug: bool = True
    database_name: str = None
    database_host: str = "localhost"
    database_username: str = None
    database_password: str = None
    database_port: str = "5432"
    CORS_ALLOWED_ORIGINS: Union[str, List[str]] = ["*"]

    database_url: Optional[str] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if isinstance(self.CORS_ALLOWED_ORIGINS, str):
            self.CORS_ALLOWED_ORIGINS = self.CORS_ALLOWED_ORIGINS.split(",")

        missing_fields = [
            field for field in [
                "database_username",
                "database_password",
                "database_host",
                "database_port",
                "database_name",
            ]
            if not getattr(self, field, None)
        ]
        if missing_fields:
            raise ValueError(f"Следующие параметры не переданы или пустые: {', '.join(missing_fields)}")

        self.database_url = f"postgresql://{self.database_username}:{self.database_password}@{self.database_host}:{self.database_port}/{self.database_name}"

    # получение данных из файла .env
    class Config:
        env_file = str(Path(__file__).parent.parent / ".env")


try:
    settings = Settings()
    # os.environ["DATABASE_URL"] = settings.database_url
except ValidationError as e:
    print("Ошибка валидации Pydantic:", e)
except ValueError as e:
    print("Ошибка инициализации настроек:", e)