from fastapi import Depends
from fastapi.responses import JSONResponse

from .auth_dependencies import get_auth_uow
from .auth_schemas import AuthRegisterIn, AuthRegisterInternal, AuthLoginIn
from .auth_uow import AuthUnitOfWork
from .utils.auth_utils import is_valid_create_user_data, success_login_user
from .utils.security import hash_password, verify_password

from ..exceptions.auth_exceptions import InvalidCredentialsException
from ..exceptions.base_exceptions import AppException
from ..models.models import User
from ..token.token_utils import delete_refresh_token_cookie


class AuthService:
    @staticmethod
    async def register_user_service(
        auth_in: AuthRegisterIn,
        auth_uow: AuthUnitOfWork = Depends(get_auth_uow)
    ):

        valid_data = is_valid_create_user_data(auth_in)
        if not valid_data[0]:
            raise AppException(detail=valid_data[1])

        hashed_password = hash_password(auth_in.password)
        auth_internal = AuthRegisterInternal(
            email=auth_in.email,
            name=auth_in.name,
            hashed_password=hashed_password,
        )

        user = await auth_uow.register_user_uow(
            auth_in=auth_internal
        )

        user_id = user.id
        response = success_login_user(user_id=user_id)

        return response

    @staticmethod
    async def login_user_service(
            auth_in: AuthLoginIn,
            auth_uow: AuthUnitOfWork = Depends(get_auth_uow)
    ):

        valid_data = is_valid_create_user_data(auth_in, check_name=False)
        if not valid_data[0]:
            raise AppException(detail=valid_data[1])

        selected_columns = User.get_columns_by_names("id", "hashed_password")

        user_data = await auth_uow.login_user_uow(
            email=auth_in.email,
            selected_columns=selected_columns
        )
        if not user_data:
            raise InvalidCredentialsException()

        user_id, user_hashed_password = user_data
        if not user_id:
            raise InvalidCredentialsException()

        if not verify_password(auth_in.password, user_hashed_password):
            raise InvalidCredentialsException()

        response = success_login_user(user_id=user_id)

        return response

    @staticmethod
    async def logout_user_service() -> JSONResponse:
        """
        Выход пользователя из системы.

        ### Логика:
        1. Удаляет refresh токен из cookies через `AuthTokenUOW`.
        2. Возвращает JSON-ответ с сообщением об успешном выходе.

        ### Возвращаемые данные:
        - `JSONResponse`:
          - Поля:
            - `message` (str): Сообщение об успешном выходе.
        """
        response = JSONResponse(
            content={
                "message": "Successfully logged out"
            })

        delete_refresh_token_cookie(response)

        return response
