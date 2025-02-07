from typing import Annotated

from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from ..authentication.utils.auth_utils import is_valid_email
from ..authentication.utils.security import verify_password
from ..exceptions.auth_exceptions import InvalidEmailException, InvalidCredentialsException
from .token_schemas import AccessTokenOut
from .token_utils import (
    create_refresh_token,
    set_refresh_token_cookie,
    create_access_token,
    create_access_token_by_refresh,
    get_sub_from_token
)
from ..exceptions.token_exceptions import TokenMissingException, InvalidTokenUserException
from ..models.models import User
from ..user.user_dependencies import get_user_repository
from ..user.user_repository import UserRepository


class TokenService:
    async def login_by_password_service(
            self,
            form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
            user_repo: UserRepository = Depends(get_user_repository)
    ) -> JSONResponse:

        if not is_valid_email(form_data.username):
            raise InvalidEmailException()

        user_data = await user_repo.get_user_id_password_by_login(
            selected_columns=User.get_columns_by_names("id", "hashed_password"),
            email=form_data.username,
        )

        if not user_data:
            raise InvalidCredentialsException()

        user_id, hashed_password = user_data
        if not user_id:
            raise InvalidCredentialsException()
        if not verify_password(form_data.password, hashed_password):
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
            request: Request,
            user_repo: UserRepository = Depends(get_user_repository)
    ):
        refresh_token = request.cookies.get("refresh_token")

        if not refresh_token:
            raise TokenMissingException("Refresh")

        user_id = get_sub_from_token(refresh_token)
        if not await user_repo.get_user_by_id(
            user_id, User.get_pk_columns()
        ):
            raise InvalidTokenUserException()

        access_token = create_access_token_by_refresh(refresh_token)

        token_out = AccessTokenOut(
            access_token=access_token
        )
        return token_out
