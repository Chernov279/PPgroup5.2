from typing import Annotated

from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from ..authentication.utils.auth_utils import is_valid_email
from ..authentication.utils.security import verify_password
from ..exceptions.auth_exceptions import InvalidEmailException, InvalidCredentialsException
from .token_dependencies import get_token_repository
from .token_repository import TokenRepository
from .token_schemas import AccessTokenOut
from .token_utils import (
    create_refresh_token,
    set_refresh_token_cookie,
    create_access_token,
    create_access_token_by_refresh
)
from ..exceptions.token_exceptions import TokenMissingException
from ..models.models import User


class TokenService:
    async def login_by_password_service(
            self,
            form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
            token_repo: TokenRepository = Depends(get_token_repository)
    ) -> JSONResponse:

        if not is_valid_email(form_data.username):
            raise InvalidEmailException()

        user_id, hashed_password = await token_repo.get_user_id_password_by_login(
            selected_column=User.get_columns_by_names("id", "hashed_password"),
            email=form_data.username,
        )

        if not verify_password(form_data.password, hashed_password):
            raise InvalidCredentialsException()

        if not user_id:
            raise InvalidCredentialsException()

        refresh_token = create_refresh_token(user_id)
        access_token = create_access_token(user_id)

        response = JSONResponse(content={
            "access_token": access_token,
            "token_type": "bearer",
        })
        set_refresh_token_cookie(response=response, refresh_token=refresh_token)
        return response

    async def get_access_token_service(
            self,
            request: Request
    ):
        """
        Получение нового access токена по refresh токену, который передаётся через cookie.

        ### Входные параметры:
        - `request` (Request): HTTP запрос, содержащий refresh токен в cookie.

        ### Логика:
        Извлекается refresh токен из cookie.
        Генерируется новый access токен через `TokenRepository`.
        Если токена нет или он недействителен, выбрасывается ошибка.

        ### Возвращаемые данные:
        - `dict`:
          - `access_token` (str): Новый access токен.
          - `token_type` (str): Тип токена, обычно "bearer".
        """
        refresh_token = request.cookies.get("refresh_token")

        if not refresh_token:
            raise TokenMissingException("Refresh")

        access_token = create_access_token_by_refresh(refresh_token)

        token_out = AccessTokenOut(
            access_token=access_token
        )
        return token_out
