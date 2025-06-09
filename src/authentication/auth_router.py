from typing import Annotated

from fastapi import Depends, APIRouter
from fastapi.responses import JSONResponse

from .auth_service import AuthService
from ..token_app.token_schemas import AccessTokenOut

auth = APIRouter(prefix="/auth", tags=["auth"])


# TODO роутер на сгенерирование пароля с заданными данными

@auth.post("/register", summary="Register a new user")
async def register_user_route(
        auth_out: Annotated[AccessTokenOut, Depends(AuthService.register_user_service)],
):
    return auth_out


@auth.post("/login", summary="Authentication user")
async def login_user_route(
        auth_out: Annotated[AccessTokenOut, Depends(AuthService.login_user_service)],
):
    return auth_out


@auth.post("/logout", summary="logout user")
async def logout_user_route(
        auth_out: Annotated[AccessTokenOut, Depends(AuthService.logout_user_service)],
):
    return auth_out
