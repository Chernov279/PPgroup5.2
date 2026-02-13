from typing import Optional

from fastapi import Body, Cookie, Request

from src.core.auth.utils.token_utils import get_sub_from_token
from src.exceptions.token_exceptions import TokenMissingException


async def get_refresh_token(
    refresh_token: Optional[str] = Body(None, embed=True),
    refresh_token_cookie: Optional[str] = Cookie(None, alias="refresh_token")
) -> str | None:
    token = refresh_token_cookie or refresh_token
    return token


def get_optional_token(request: Request) -> Optional[str]:
    """
    Получает токен из заголовка Authorization.
    Если токена нет — просто возвращает None, без ошибки 401.
    """
    authorization: Optional[str] = request.headers.get("Authorization")
    if authorization and authorization.startswith("Bearer "):
        return authorization.split("Bearer ")[1]
    return None


def get_token_sub_required(request: Request) -> Optional[int]:
    """
    Получает значение sub - обычно user_id - из заголовка Authorization через токен.
    Если токена нет — возвращает ошибку.
    """
    token = get_optional_token(request)
    if token is None:
        raise TokenMissingException()
    sub = get_sub_from_token(token, raise_exception=True)
    return sub


def get_token_sub_optional(request: Request) -> Optional[int]:
    """
    Получает значение sub - обычно user_id - из заголовка Authorization через токен.
    Если токена нет ли он невалидный — просто возвращает None, без ошибки.
    """
    token = get_optional_token(request)
    if token is None:
        return None

    sub = get_sub_from_token(token, raise_exception=False)
    return sub