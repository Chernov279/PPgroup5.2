from fastapi import Depends, APIRouter

from src.authentication.auth_dependecies import get_user_auth_service
from src.authentication.auth_service import UserAuthService
from src.authentication.schemas import UserAuthIn, UserLoginIn, UserLoginOut, TokenOut
from src.services.token_service import TokenService
from src.dependencies.token_dependencies import get_token_service

auth = APIRouter(prefix="/auth", tags=["auth"])


@auth.post("/register", response_model=UserLoginOut, summary="Register a new user")
def register_user_route(
    user_auth: UserAuthIn,
    user_auth_service: UserAuthService = Depends(get_user_auth_service),
):
    """
    Регистрация нового пользователя.
    """
    return user_auth_service.register_user(user_auth.name, user_auth.email, user_auth.password)


@auth.post("/login", response_model=UserLoginOut, summary="Authentication user")
def register_user_route(
    user_login: UserLoginIn,
    user_auth_service: UserAuthService = Depends(get_user_auth_service),
):
    """
    Авторизация пользователя.
    """
    return user_auth_service.login_user(user_login.email, user_login.password)


@auth.post("/get_token", response_model=TokenOut, summary="get access token by refresh token")
def register_user_route(
    refresh_token: str | None,
    token_service: TokenService = Depends(get_token_service),
):
    """
    Получение access_token по refresh_token.
    """
    return token_service.create_access_token_service(refresh_token)
