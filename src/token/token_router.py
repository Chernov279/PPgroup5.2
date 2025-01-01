from typing import Annotated

from fastapi import Depends, APIRouter, Request
from fastapi.security import OAuth2PasswordRequestForm

from .token_dependencies import get_token_db_service, get_token_service
from .token_service import TokenService
from ..authentication.auth_schemas import AccessTokenOut

token = APIRouter(tags=["token"])


@token.post("/token", response_model=AccessTokenOut, summary="logining by email and password, returns tokens")
def login_by_token_route(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        token_service: TokenService = Depends(get_token_db_service),
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
    return token_service.login_user_service(form_data)


@token.post("/get_token", response_model=AccessTokenOut, summary="get access token by refresh token")
def get_access_token_route(
        request: Request,
        token_service: TokenService = Depends(get_token_service),
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
    return token_service.get_access_token_service(request)
