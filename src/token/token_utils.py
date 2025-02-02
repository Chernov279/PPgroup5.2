from datetime import timedelta, datetime
from typing import Optional

import jwt
from fastapi import HTTPException

from ..config.token_config import settings_token
from ..exceptions.token_exceptions import InvalidTokenUserException


def create_access_jwt_token(
        data: dict | None = None,
        user_id: int | None = None,
        expires_delta: timedelta | None = None) -> str:
    """
    Генерация access JWT токена.

    ### Входные параметры:
    - `data` (dict | None): Дополнительные данные для токена. Обязательно должен хранить user_id, если передается.
    - `user_id` (int | None): Идентификатор пользователя.
    - `expires_delta` (timedelta | None): Время жизни токена. Если не передано, используется значение по умолчанию.

    ### Возвращаемые данные:
    - `str`: Сгенерированный access токен.
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings_token.ACCESS_TOKEN_EXPIRE_MINUTES)
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

    ### Входные параметры:
    - `data` (dict | None): Дополнительные данные для токена.
    - `user_id` (int | None): Идентификатор пользователя.
    - `expires_delta` (timedelta | None): Время жизни токена. Если не передано, используется значение по умолчанию.

    ### Возвращаемые данные:
    - `str`: Сгенерированный refresh токен.
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=settings_token.REFRESH_TOKEN_EXPIRE_DAYS)
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

    ### Входные параметры:
    - `token` (str): Токен.

    ### Логика:
    1. Декодирует токен и проверяет его на валидность.
    2. Если токен истёк или повреждён, вызывает исключение.

    ### Возвращаемые данные:
    - `dict`: Декодированный payload токена.
    - `None`: Если токен недействителен или истёк.
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


def get_sub_from_token(token) -> Optional[int]:
    payload = verify_jwt_token(token)
    user_id = payload.get("sub", None)
    if not user_id:
        # Это нормальная ситуация для утилиты, так как обработка токена может завершиться ошибкой
        raise InvalidTokenUserException()
    return int(user_id)

