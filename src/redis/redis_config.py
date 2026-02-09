from typing import Optional, List

from pydantic import ValidationError, ConfigDict
from pydantic_settings import BaseSettings
from pathlib import Path


class ConfigRedis(BaseSettings):

    REDIS_HOST: str = "localhost"
    REDIS_PORT: str = "6379"
    REDIS_DBS: List[str] = ["0"]
    REDIS_PASSWORD: Optional[str] = None

    REDIS_URL0: Optional[str] = None
    REDIS_URL1: Optional[str] = None


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if self.REDIS_URL0:
            return

        missing_fields = [
            field for field in [
                "REDIS_HOST",
                "REDIS_PORT",
                "REDIS_DBS",
            ]
            if not getattr(self, field, None)
        ]
        if missing_fields:
            raise ValueError(f"Следующие параметры не переданы или пустые: {', '.join(missing_fields)}")
        if self.REDIS_PASSWORD:
            self.REDIS_URL0 = f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DBS[0]}"
        else:
            self.REDIS_URL0 = f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DBS[0]}"

        if len(self.REDIS_DBS)>1:
            if self.REDIS_PASSWORD:
                self.REDIS_URL1 = f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DBS[1]}"
            else:
                self.REDIS_URL1 = f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DBS[1]}"


try:
    settings_redis = ConfigRedis()
except ValidationError as e:
    print("Ошибка валидации Pydantic:", e)
except ValueError as e:
    print("Ошибка инициализации настроек:", e)
