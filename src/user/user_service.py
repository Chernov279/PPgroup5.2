from typing import Annotated

from fastapi import Depends

from .user_activity_service import UserActivityService
from .user_dependencies import get_user_uow
from .user_uow import UserUnitOfWork
from .user_schemas import (
    UserCreateIn,
    UserUpdateIn,
    UserDetailOut,
    UserShortOut, UserPrimaryKey
)

from ..config.token_config import oauth2_scheme
from ..exceptions.user_exceptions import (
    UserNotFoundException,
    UserDeletedSuccessException,
    UserFailedUpdateException,
    UserFailedCreateException,
    UserFailedDeleteException
)
from ..schemas.database_params_schemas import MultiGetParams
from ..token.token_dependencies import get_optional_token
from ..token.token_utils import get_sub_from_token
from ..utils.schema_utils import delete_none_params


class UserService:
    @staticmethod
    async def get_all_users_service(
            token: Annotated[str, Depends(get_optional_token)],
            multi_get_params: MultiGetParams = Depends(),
            user_uow: UserUnitOfWork = Depends(get_user_uow)
    ):
        token_user_id = get_sub_from_token(token=token, raise_exception=False)

        async with user_uow as uow:
            users = await uow.get_all_users_uow(
                **multi_get_params.model_dump(),
                selected_columns=UserShortOut.get_selected_columns()
            )

            if token_user_id is not None:
                await UserActivityService(user_repository=uow.repository).update_user_activity_service(token_user_id)
        return users

    @staticmethod
    async def get_user_by_id_service(
            token: Annotated[str, Depends(get_optional_token)],
            user_id: UserPrimaryKey = Depends(),
            user_uow: UserUnitOfWork = Depends(get_user_uow)
    ):
        token_user_id = get_sub_from_token(token=token, raise_exception=False)
        selected_columns = UserDetailOut.get_selected_columns()

        async with user_uow as uow:
            user = await uow.get_user_by_id_uow(user_id, selected_columns)
            if not user:
                raise UserNotFoundException(user_id)
            if token_user_id is not None:
                await UserActivityService(user_repository=uow.repository).update_user_activity_service(token_user_id)
            await uow.commit()
            return user

    @staticmethod
    async def get_user_me_service(
            token: Annotated[str, Depends(oauth2_scheme)],
            user_uow: UserUnitOfWork = Depends(get_user_uow)
    ):
        token_user_id = get_sub_from_token(token)
        selected_columns = UserDetailOut.get_selected_columns()

        async with user_uow as uow:
            user = await uow.get_user_by_id_uow(token_user_id, selected_columns)
            if not user:
                raise UserNotFoundException(token_user_id)
            if token_user_id is not None:
                await UserActivityService(user_repository=uow.repository).update_user_activity_service(token_user_id)
            await uow.commit()
            return user

    @staticmethod
    async def create_user_service(
            user_in: UserCreateIn,
            user_uow: UserUnitOfWork = Depends(get_user_uow)
    ):
        async with user_uow as uow:
            user = await uow.create_user_uow(user_in)
            if not user:
                raise UserFailedCreateException()
            return user

    @staticmethod
    async def update_user_service(
            user_in: UserUpdateIn,
            token: Annotated[str, Depends(oauth2_scheme)],
            user_uow: UserUnitOfWork = Depends(get_user_uow)
    ):
        user_id = get_sub_from_token(token)
        delete_none_params(user_in)
        async with user_uow as uow:
            user = await uow.update_user_uow(user_in, user_id)
            if not user:
                raise UserFailedUpdateException()
            return user

    @staticmethod
    async def delete_user_service(
            token: Annotated[str, Depends(oauth2_scheme)],
            user_uow: UserUnitOfWork = Depends(get_user_uow)
    ):
        user_id = get_sub_from_token(token)

        async with user_uow as uow:
            is_deleted = await uow.delete_user_uow(user_id)
            if is_deleted:
                raise UserDeletedSuccessException(user_id)
            raise UserFailedDeleteException()
