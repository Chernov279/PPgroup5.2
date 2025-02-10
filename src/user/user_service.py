from typing import Annotated

from fastapi import Depends

from .user_dependencies import get_user_uow
from .user_uow import UserUnitOfWork
from .user_schemas import UserCreateIn, UserUpdateIn, UserDetailOut, UserShortOut

from ..config.token_config import oauth2_scheme
from ..exceptions.user_exceptions import UserNotFoundException, UserFailedActionException, UserDeletedSuccessException
from ..token.token_utils import get_sub_from_token
from ..utils.schema_utils import delete_none_params


# TODO is_active -> все проходит через uow, BaseService

class UserService:
    @staticmethod
    async def get_all_users_service(
            limit: int = 30,
            offset: int = 0,
            user_uow: UserUnitOfWork = Depends(get_user_uow)
    ):
        limit = max(1, min(50, limit))
        offset = max(1, offset)  # int32
        selected_columns = UserShortOut.get_selected_columns()

        async with user_uow as uow:
            users = await uow.get_all_users_uow(limit, offset, selected_columns)
        return users

    @staticmethod
    async def get_user_by_id_service(
            user_id: int,
            user_uow: UserUnitOfWork = Depends(get_user_uow)
    ):
        selected_columns = UserDetailOut.get_selected_columns()

        async with user_uow as uow:
            user = await uow.get_user_by_id_uow(user_id, selected_columns)
            if not user:
                raise UserNotFoundException(user_id)
            return user

    @staticmethod
    async def get_user_me_service(
            token: Annotated[str, Depends(oauth2_scheme)],
            user_uow: UserUnitOfWork = Depends(get_user_uow)
    ):
        user_id = get_sub_from_token(token)
        selected_columns = UserDetailOut.get_selected_columns()

        async with user_uow as uow:
            user = await uow.get_user_by_id_uow(user_id, selected_columns)
            if not user:
                raise UserNotFoundException(user_id)
            return user

    @staticmethod
    async def create_user_service(
            user_in: UserCreateIn,
            user_uow: UserUnitOfWork = Depends(get_user_uow)
    ):
        async with user_uow as uow:
            user = await uow.create_user_uow(user_in)
            if not user:
                raise UserFailedActionException("create user")
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
                raise UserFailedActionException("update user")
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
            raise UserFailedActionException("delete user")
