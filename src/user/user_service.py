import logging
import asyncio

from fastapi import Depends

from .user_dependencies import get_user_uow
from .user_uow import UserUnitOfWork
from .user_schemas import (
    UserUpdateIn,
    UserDetailOut,
    UserShortOut,
    UserPrimaryKey
)

from ..exceptions.user_exceptions import (
    UserNotFoundException,
    UserDeletedSuccessException,
    UserFailedUpdateException,
    UserFailedDeleteException
)
from ..kafka.producers.user_activity import user_activity_producer
from ..schemas.database_params_schemas import MultiGetParams
from ..token_app.token_utils import get_sub_from_token
from ..utils.schema_utils import delete_none_params

logger = logging.getLogger(__name__)


class UserService:
    def __init__(
            self,
            user_uow: UserUnitOfWork = Depends(get_user_uow)
    ):
        self._uow = user_uow

    async def get_all_users(
            self,
            token: str,
            multi_get_params: MultiGetParams,
    ):
        token_user_id = get_sub_from_token(token=token, raise_exception=False)
        logger.info("Incoming request to get_all_users sub=%s", token_user_id)

        users = await self._uow.get_all_users_uow(
            **multi_get_params.model_dump(),
            selected_columns=UserShortOut.get_selected_columns()
        )

        if token_user_id is not None:
            asyncio.create_task(user_activity_producer.send_user_activity(
                "user_get_all",
                token_user_id
            ))
        return users

    async def get_user_by_id(
            self,
            token: str,
            userPK: UserPrimaryKey,
    ):
        token_user_id = get_sub_from_token(token=token, raise_exception=False)
        logger.info("Incoming request to get_user_by_id sub=%s", token_user_id)

        selected_columns = UserDetailOut.get_selected_columns()
        user_id = userPK.id

        user = await self._uow.get_user_by_id_uow(user_id, selected_columns)

        if token_user_id is not None:
            asyncio.create_task(user_activity_producer.send_user_activity(
                "user_get_user_by_id",
                token_user_id
            ))

        if not user:
            raise UserNotFoundException(user_id)
        return user

    async def get_user_me(
            self,
            token: str,
    ):
        token_user_id = get_sub_from_token(token)
        logger.info("Incoming request to get_user_me sub=%s", token_user_id)

        selected_columns = UserDetailOut.get_selected_columns()

        user = await self._uow.get_user_by_id_uow(token_user_id, selected_columns)

        if not user:
            raise UserNotFoundException(token_user_id)

        asyncio.create_task(user_activity_producer.send_user_activity(
            "user_get_me",
            token_user_id
        ))
        return user

    async def update_user(
            self,
            user_in: UserUpdateIn,
            token: str
    ):
        token_user_id = get_sub_from_token(token)
        logger.info("Incoming request to update_user sub=%s", token_user_id)
        delete_none_params(user_in)

        user = await self._uow.update_user_uow(user_in, token_user_id)

        if not user:
            raise UserFailedUpdateException()

        asyncio.create_task(user_activity_producer.send_user_activity(
            "user_update",
            token_user_id
        ))

        return user

    async def delete_user(
            self,
            token: str,
    ):
        token_user_id = get_sub_from_token(token)
        logger.info("Incoming request to update_user sub=%s", token_user_id)

        is_deleted = await self._uow.delete_user_uow(token_user_id)
        if is_deleted:
            raise UserDeletedSuccessException(token_user_id)
        raise UserFailedDeleteException()
