from datetime import timedelta, datetime
from typing import Optional, Union

import jwt
from fastapi import HTTPException

from ..config.token_config import settings_token
from ..exceptions.token_exceptions import InvalidTokenUserException


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
        max_age=settings_token.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        path="/get_token",
    )


def delete_refresh_token_cookie_uow(response) -> None:
    """
    Удаляет refresh токен из cookies.

    ### Входные параметры:
    - `response` (JSONResponse): Ответ, из которого нужно удалить cookie.

    ### Логика:
    1. Удаляет cookie с ключом `refresh_token` и путем `/get_token`.
    """
    response.delete_cookie(
        key="refresh_token",
        path="/get_token"
    )


def create_access_token_by_refresh(refresh_token: str) -> str | None:
    """
    Создание access токена на основе переданного refresh токена.

    ### Входные параметры:
    - `refresh_token` (str): Refresh токен.

    ### Логика:
    1. Проверяется валидность refresh токена.
    2. Генерируется новый access токен, на основе данных из refresh токена.

    ### Возвращаемые данные:
    - `str`: Сгенерированный access токен.
    """
    payload = verify_jwt_token(refresh_token)
    if payload.get("type", "") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid token")
    return create_access_jwt_token(payload)


def create_refresh_token(user_id: Union[int, str]) -> str | None:
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
    refresh_token = create_refresh_jwt_token(user_id=user_id)
    return refresh_token


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
        raise InvalidTokenUserException()
    if isinstance(user_id, str):
        return int(user_id)
    elif isinstance(user_id, int):
        return user_id
    raise HTTPException(status_code=415, detail="sub from token is unsupported type")
