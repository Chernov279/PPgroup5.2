from typing import Annotated

from fastapi import Depends, APIRouter

from src.authentication.auth_dependecies import get_user_auth_service
from src.authentication.auth_service import UserAuthService
from src.authentication.schemas import UserAuthIn, UserLoginIn, AccessTokenOut, TokensOut
from src.models.models import User
from src.token.token_service import TokenService

auth = APIRouter(prefix="/auth", tags=["auth"])


# @auth.post("/register", response_model=AccessTokenOut, summary="Register a new user")
# def register_user_route(
#     user_auth: UserAuthIn,
#     user_auth_service: UserAuthService = Depends(get_user_auth_service),
# ):
#     """
#     Регистрация нового пользователя.
#     """
#     return user_auth_service.register_user(user_auth.name, user_auth.email, user_auth.password)
#
#
# @auth.post("/login", response_model=AccessTokenOut, summary="Authentication user")
# def login_user_route(
#     user_login: UserLoginIn,
#     user_auth_service: UserAuthService = Depends(get_user_auth_service),
# ):
#     """
#     Авторизация пользователя.
#     """
#     return user_auth_service.login_user(user_login.email, user_login.password)
#
#
# @auth.get("/users/me")
# def read_users_me(
#     current_user: Annotated[User, Depends(TokenService.get_user_by_token_service)],
# ):
#     return current_user