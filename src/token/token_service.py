from typing import Annotated

from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from .token_dependencies import get_token_uow
from .token_uow import TokenUnitOfWork
from .token_schemas import AccessTokenOut
from .token_utils import (
    create_refresh_token,
    set_refresh_token_cookie,
    create_access_token,
    create_access_token_by_refresh,
    get_sub_from_token
)

from ..authentication.utils.auth_utils import is_valid_email
from ..authentication.utils.security import verify_password
from ..exceptions.auth_exceptions import InvalidEmailException, InvalidCredentialsException
from ..exceptions.token_exceptions import TokenMissingException, InvalidTokenUserException
from ..models.models import User


class TokenService:
    @staticmethod
    async def login_by_password_service(
            form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
            token_uow: TokenUnitOfWork = Depends(get_token_uow)
    ) -> JSONResponse:
        if not is_valid_email(form_data.username):
            raise InvalidEmailException()

        async with token_uow as uow:
            user_data = await uow.login_by_password_uow(
                email=form_data.username,
                selected_columns=User.get_columns_by_names("id", "hashed_password"),
            )

        if not user_data:
            raise InvalidCredentialsException()

        user_id, hashed_password = user_data.id, user_data.hashed_password

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

    @staticmethod
    async def get_access_token_service(
            request: Request,
            token_uow: TokenUnitOfWork = Depends(get_token_uow)
    ):
        refresh_token = request.cookies.get("refresh_token")

        if not refresh_token:
            raise TokenMissingException("Refresh")

        user_id = get_sub_from_token(refresh_token)

        async with token_uow as uow:
            if not await uow.get_access_token_uow(
                user_id, User.get_pk_columns()
            ):
                raise InvalidTokenUserException()

        access_token = create_access_token_by_refresh(refresh_token)

        token_out = AccessTokenOut(
            access_token=access_token
        )
        return token_out
