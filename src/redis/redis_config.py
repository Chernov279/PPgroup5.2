from typing import Optional

from pydantic import ValidationError, ConfigDict
from pydantic_settings import BaseSettings
from pathlib import Path


class ConfigRedis(BaseSettings):

    REDIS_HOST: str = "localhost"
    REDIS_PORT: str = "6379"
    REDIS_DB: str = "0"
    REDIS_PASSWORD: Optional[str] = None

    REDIS_URL: Optional[str] = None

    # получение данных из файла .env
    model_config = {
        "env_file": str(Path(__file__).parent.parent.parent / ".env"),
        "extra": "ignore"
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if self.REDIS_URL:
            return

        missing_fields = [
            field for field in [
                "REDIS_HOST",
                "REDIS_PORT",
                "REDIS_DB",
            ]
            if not getattr(self, field, None)
        ]
        if missing_fields:
            raise ValueError(f"Следующие параметры не переданы или пустые: {', '.join(missing_fields)}")
        if self.REDIS_PASSWORD:
            self.REDIS_URL = f"redis://:{settings_redis.REDIS_PASSWORD}@{settings_redis.REDIS_HOST}:{settings_redis.REDIS_PORT}/{settings_redis.REDIS_DB}"
        else:
            self.REDIS_URL = f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"


try:
    settings_redis = ConfigRedis()
except ValidationError as e:
    print("Ошибка валидации Pydantic:", e)
except ValueError as e:
    print("Ошибка инициализации настроек:", e)
