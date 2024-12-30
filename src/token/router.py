from typing import Annotated

from fastapi import Depends, APIRouter, Request
from fastapi.security import OAuth2PasswordRequestForm

from src.authentication.schemas import AccessTokenOut
from src.dependencies.token_dependencies import get_token_db_service, get_token_service
from src.token.token_service import TokenService

token = APIRouter(tags=["token"])


@token.post("/token", response_model=AccessTokenOut, summary="logining by email and password, returns tokens")
def login_by_token_route(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        token_service: TokenService = Depends(get_token_db_service),
):
    return token_service.login_user_service(form_data)


@token.post("/get_token", response_model=AccessTokenOut, summary="get access token by refresh token")
def get_access_token_route(
        request: Request,
        token_service: TokenService = Depends(get_token_service),
):
    """
    Получение нового access_token по refresh_token, который передаётся через cookie.

    Инструкция:
    1. refresh_token должен быть сохранён в cookie (HttpOnly).
    2. Access токен возвращается в теле ответа.
    """
    return token_service.get_access_token_service(request)

