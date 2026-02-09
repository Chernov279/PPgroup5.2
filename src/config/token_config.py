from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from pydantic_settings import BaseSettings
from pathlib import Path

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


class TokenSettings(BaseSettings):
    # получение чувствительных данных из корневой папки

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int


try:
    settings_token = TokenSettings()
except ValidationError as e:
    print("Ошибка валидации Pydantic:", e)
except ValueError as e:
    print("Ошибка инициализации настроек:", e)
