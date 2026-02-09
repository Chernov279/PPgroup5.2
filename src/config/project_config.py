from typing import List, Union

from pydantic import ValidationError
from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    # получение чувствительных данных из корневой папки

    PROJECT_NAME: str = "Unnamed Project"
    DEBUG: bool = True
    VERSION: str = "1.0"
    CORS_ALLOWED_ORIGINS: Union[str, List[str]] = ["*"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if isinstance(self.CORS_ALLOWED_ORIGINS, str):
            self.CORS_ALLOWED_ORIGINS = self.CORS_ALLOWED_ORIGINS.split(",")

        missing_fields = [
            field for field in [
                "PROJECT_NAME",
                "DEBUG",
                "VERSION"
            ]
            if getattr(self, field, None) is None
        ]
        if missing_fields:
            raise ValueError(f"Следующие параметры не переданы или пустые: {', '.join(missing_fields)}")


try:
    settings_project = Settings()
except ValidationError as e:
    print("Ошибка валидации Pydantic:", e)
except ValueError as e:
    print("Ошибка инициализации настроек:", e)