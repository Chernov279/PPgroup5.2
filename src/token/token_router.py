from typing import Annotated

from fastapi import Depends, APIRouter

from .token_service import TokenService
from ..authentication.auth_schemas import AccessTokenOut

token = APIRouter(tags=["token"])


@token.post("/token", response_model=AccessTokenOut, summary="logining by email and password, returns tokens")
async def login_by_password_route(
        token_out: Annotated[AccessTokenOut, Depends(TokenService.login_by_password_service)],
):
    """
    Авторизация пользователя с использованием email и пароля. Возвращает access и refresh токены.
    Нужна для добавления кнопки авторизации в сваггере

    ### Входные параметры:
    - `form_data` (OAuth2PasswordRequestForm):
      - `username` (str): Email пользователя.
      - `password` (str): Пароль пользователя.

    ### Логика:
    1. Входные данные передаются в сервис `TokenService`.
    2. Сервис проверяет данные пользователя, генерирует токены.
    3. Возвращает JSON-ответ с access токеном.

    ### Возвращаемые данные:
    - `response_model`: `AccessTokenOut`:
      - `access_token` (str): Сгенерированный access токен.
      - `token_type` (str): Тип токена, обычно "bearer".
    """
    return token_out


@token.post("/get_token", response_model=AccessTokenOut, summary="get access token by refresh token")
async def get_access_token_route(
        token_out: Annotated[AccessTokenOut, Depends(TokenService.get_access_token_service)],
):
    """
    Получение нового access токена по refresh токену, который передается через cookie.

    ### Инструкция:
    1. Refresh токен должен быть сохранён в cookie (HttpOnly).
    2. В ответ возвращается новый access токен.

    ### Логика:
    1. Токен передается в сервис `TokenService`.
    2. Сервис генерирует новый access токен, используя refresh токен.

    ### Возвращаемые данные:
    - `response_model`: `AccessTokenOut`:
      - `access_token` (str): Новый access токен.
      - `token_type` (str): Тип токена, обычно "bearer".
    """
    return token_out

# TODO"выйти со всех устройств", типа чтобы все токены резко стали нерабочими. Что если записывать к каждому токену дату его создания. Тогда можно при нажатии выйти со всех устройств добавить в бд время нажатия на выход и рефреш токены которые были созданы до этого времени сделать нерабочими. Как тебе выход?
