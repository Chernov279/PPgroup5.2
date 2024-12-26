from datetime import datetime, timedelta
from passlib.context import CryptContext
import jwt

from fastapi import HTTPException

from src.config.token_config import settings_token


def create_access_jwt_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Генерация JWT токена.
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(settings_token.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = data.copy()
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings_token.SECRET_KEY, algorithm=settings_token.ALGORITHM)
    return encoded_jwt


def create_refresh_jwt_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Генерация JWT токена.
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(settings_token.REFRESH_TOKEN_EXPIRE_DAYS)

    to_encode = data.copy()
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings_token.SECRET_KEY, algorithm=settings_token.ALGORITHM)
    return encoded_jwt


def verify_jwt_token(token: str) -> dict | None:
    """
    Проверка валидности JWT токена.
    """
    try:
        decoded_jwt = jwt.decode(token, settings_token.SECRET_KEY, algorithms=[settings_token.ALGORITHM])
        return decoded_jwt
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=401, detail="Token not decoded")


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Хэширование пароля с использованием bcrypt.
    Возвращает хэшированный пароль.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Проверка пароля с хэшированным значением.
    """
    return pwd_context.verify(plain_password, hashed_password)
