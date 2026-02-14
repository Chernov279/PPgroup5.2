import secrets
from datetime import timedelta, datetime, timezone
from hashlib import sha256
from typing import Optional, Union

import jwt
from fastapi import HTTPException

from src.config import settings
from src.exceptions.token_exceptions import InvalidTokenUserException




def set_refresh_token_cookie(response, refresh_token: str) -> None:
    """
    Устанавливает refresh токен в cookies.

    ### Входные параметры:
    - `response` (JSONResponse): Ответ, в который нужно добавить cookie.
    - `refresh_token` (str): Значение refresh токена.

    ### Логика:
    Устанавливает cookie с ключом `refresh_token`.
    """
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        path="/get_token",
    )


def delete_refresh_token_cookie(response) -> None:
    """
    Удаляет refresh токен из cookies.

    ### Входные параметры:
    - `response` (JSONResponse): Ответ, из которого нужно удалить cookie.

    ### Логика:
    1. Удаляет cookie с ключом `refresh_token` и путем `/get_token`.
    """
    response.delete_cookie(
        key="refresh_token",
        path="/refresh"
    )


def create_random_token(length: int = 64) -> str:
    """
    Создает случайный токен для использования как refresh токен.

    Args:
        length: Длина токена в байтах (до генерации hex)

    Returns:
        Случайная строка в hex формате
    """
    return secrets.token_hex(length // 2)


def create_refresh_token() -> str:
    """
    Создает случайный refresh токен (не JWT).

    Returns:
        Случайный refresh токен
    """
    return create_random_token(64)

def hash_refresh_token(refresh_token: str) -> str:
    """
    Хэширует заданным алгоритмом refresh токен.

    Returns:
        Захэшированный refresh токен
    """
    return sha256(refresh_token.encode()).hexdigest()

def create_access_token(user_id: Union[int, str]) -> str | None:
    """
    Создание refresh токена для пользователя.

    ### Входные параметры:
    - `user_id` (int | str): Идентификатор пользователя.

    ### Логика:
    1. Проверяется валидность `user_id`.
    2. Генерируется новый refresh токен.

    ### Возвращаемые данные:
    - `str`: Сгенерированный refresh токен.
    """
    if isinstance(user_id, str):
        user_id = int(user_id)
    access_token = create_access_jwt_token(user_id=user_id)
    return access_token


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
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    if data is not None:
        to_encode = data.copy()
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt
    data = {
        "sub": f'{user_id}' if user_id else "",
        "exp": expire,
        "type": "access"
    }

    encoded_jwt = jwt.encode(data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_jwt_token(token: str) -> dict:
    """
    Проверка валидности JWT токена.

    ### Входные параметры:
    - `token` (str): Токен.

    ### Логика:
    1. Декодирует токен и проверяет его на валидность.
    2. Если токен истёк или повреждён, вызывает исключение.

    ### Возвращаемые данные:
    - `dict`: Декодированный payload токена.
    -Exception: Если токен недействителен или истёк.
    """
    try:
        decoded_jwt = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return decoded_jwt
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception:
        raise HTTPException(status_code=401, detail="Token not decoded")


def get_sub_from_token(token, raise_exception: bool = True) -> Optional[int]:
    try:
        payload = verify_jwt_token(token)
        user_id = payload.get("sub")
        if not user_id:
            raise InvalidTokenUserException()
        if isinstance(user_id, str):
            return int(user_id)
        elif isinstance(user_id, int):
            return user_id
        raise HTTPException(status_code=415, detail="sub from token is unsupported type")
    except Exception as e:
        if raise_exception:
            raise e
        else:
            return None

def get_token_expires_at():
    return datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)