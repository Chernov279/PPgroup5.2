from typing import Annotated

from fastapi import Depends

from .user_dependencies import get_user_repository, get_user_uow
from .user_repository import UserRepository
from .user_uow import UserUnitOfWork
from .user_schemas import UserCreateIn, UserUpdateIn, UserUpdateInternal, UserDetailOut, UserShortOut

from ..config.token_config import oauth2_scheme
from ..exceptions.user_exceptions import UserNotFoundException, UserFailedActionException, UserDeletedSuccessException
from ..models.models import User
from ..token.token_utils import get_sub_from_token
from ..utils.schema_utils import add_internal_params, get_selected_columns


#TODO is_active -> все проходит через uow, BaseService

class UserService:
    async def get_all_users_service(
            self,
            limit: int = 30,
            offset: int = 0,
            user_repo: UserRepository = Depends(get_user_repository)
    ):
        limit = max(1, min(50, limit))
        offset = max(1, offset)#int32
        selected_columns = get_selected_columns(UserShortOut, User)
        users = await user_repo.get_all_users(limit, offset, selected_columns)
        return users

    async def get_user_by_id_service(
            self,
            user_id: int,
            user_repo: UserRepository = Depends(get_user_repository)
    ):
        selected_columns = get_selected_columns(UserDetailOut, User)
        user = await user_repo.get_user_by_id(user_id, selected_columns)
        if not user:
            raise UserNotFoundException(user_id)
        return user

    async def get_user_me_service(
            self,
            token: Annotated[str, Depends(oauth2_scheme)],
            user_repo: UserRepository = Depends(get_user_repository)
    ):
        user_id = get_sub_from_token(token)
        selected_columns = get_selected_columns(UserDetailOut, User)
        user = await user_repo.get_user_by_id(user_id, selected_columns)
        if not user:
            raise UserNotFoundException(user_id)
        return user

    async def create_user_service(
            self,
            user_in: UserCreateIn,
            user_uow: UserUnitOfWork = Depends(get_user_uow)
    ):
        user = await user_uow.create_user_uow(user_in)
        if not user:
            raise UserFailedActionException("create user")
        return user

    async def update_user_service(
            self,
            user_in: UserUpdateIn,
            token: Annotated[str, Depends(oauth2_scheme)],
            user_uow: UserUnitOfWork = Depends(get_user_uow)
    ):
        user_id = get_sub_from_token(token)
        user_internal = add_internal_params(user_in, UserUpdateInternal, id=user_id)

        async with user_uow as uow:
            user = await uow.update_user_uow(user_internal)
            if not user:
                raise UserFailedActionException("update user")
            return user

    async def delete_user_service(
            self,
            token: Annotated[str, Depends(oauth2_scheme)],
            user_uow: UserUnitOfWork = Depends(get_user_uow)
    ):
        user_id = get_sub_from_token(token)

        async with user_uow as uow:
            is_deleted = await uow.delete_user_uow(user_id)
            if is_deleted:
                raise UserDeletedSuccessException(user_id)
            raise UserFailedActionException("delete user")
