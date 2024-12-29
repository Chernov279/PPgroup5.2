from datetime import timedelta, datetime

import jwt
from fastapi import HTTPException

from src.config.token_config import settings_token


def create_access_jwt_token(
        data: dict | None = None,
        user_id: int | None = None,
        expires_delta: timedelta | None = None) -> str:
    """
    Генерация access JWT токена.
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(settings_token.ACCESS_TOKEN_EXPIRE_MINUTES)
    if data is not None:
        to_encode = data.copy()
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings_token.SECRET_KEY, algorithm=settings_token.ALGORITHM)
        return encoded_jwt
    data = {
        "sub": f'{user_id}' if user_id else "",
        "exp": expire,
        "type": "access"
    }

    encoded_jwt = jwt.encode(data, settings_token.SECRET_KEY, algorithm=settings_token.ALGORITHM)
    return encoded_jwt


def create_refresh_jwt_token(
        data: dict | None = None,
        user_id: int | None = None,
        expires_delta: timedelta | None = None) -> str:
    """
    Генерация refresh JWT токена.
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(settings_token.REFRESH_TOKEN_EXPIRE_DAYS)
    if data is not None:
        to_encode = data.copy()
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings_token.SECRET_KEY, algorithm=settings_token.ALGORITHM)
        return encoded_jwt
    data = {
        "sub": f'{user_id}' if user_id else "",
        "exp": expire,
        "type": "refresh"
    }

    encoded_jwt = jwt.encode(data, settings_token.SECRET_KEY, algorithm=settings_token.ALGORITHM)
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
