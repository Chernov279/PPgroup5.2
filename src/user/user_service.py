from typing import Annotated

from fastapi import Depends

from src.user_activity.user_activity_service import UserActivityService
from .kafka_producer import user_kafka_producer
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
from ..token_app.token_dependencies import get_optional_token
from ..token_app.token_utils import get_sub_from_token
from ..utils.schema_utils import delete_none_params


class UserService:
    @staticmethod
    async def get_all_users_service(
            token: Annotated[str, Depends(get_optional_token)],
            multi_get_params: MultiGetParams = Depends(),
            user_uow: UserUnitOfWork = Depends(get_user_uow)
    ):
        token_user_id = get_sub_from_token(token=token, raise_exception=False)

        users = await user_uow.get_all_users_uow(
            **multi_get_params.model_dump(),
            selected_columns=UserShortOut.get_selected_columns()
        )

        if token_user_id is not None:
            await user_kafka_producer.send_data({
                "event_name": "user_get_all",
                "user_id": token_user_id
            })
        return users

    @staticmethod
    async def get_user_by_id_service(
            token: Annotated[str, Depends(get_optional_token)],
            userPK: UserPrimaryKey = Depends(),
            user_uow: UserUnitOfWork = Depends(get_user_uow)
    ):
        token_user_id = get_sub_from_token(token=token, raise_exception=False)
        selected_columns = UserDetailOut.get_selected_columns()
        user_id = userPK.id

        user = await user_uow.get_user_by_id_uow(user_id, selected_columns)

        if token_user_id is not None:
            await user_kafka_producer.send_data({
                "event_name": "user_get_user",
                "user_id": token_user_id
            })

        if not user:
            raise UserNotFoundException(user_id)
        return user

    @staticmethod
    async def get_user_me_service(
            token: Annotated[str, Depends(oauth2_scheme)],
            user_uow: UserUnitOfWork = Depends(get_user_uow)
    ):
        token_user_id = get_sub_from_token(token)
        selected_columns = UserDetailOut.get_selected_columns()

        user = await user_uow.get_user_by_id_uow(token_user_id, selected_columns)
        if not user:
            raise UserNotFoundException(token_user_id)
        if token_user_id is not None:
            await user_kafka_producer.send_data({
                "event_name": "user_get_me",
                "user_id": token_user_id
            })
        return user

    @staticmethod
    async def create_user_service(
            user_in: UserCreateIn,
            user_uow: UserUnitOfWork = Depends(get_user_uow)
    ):
        user = await user_uow.create_user_uow(user_in)
        if not user:
            raise UserFailedCreateException()
        await user_kafka_producer.send_data({
            "event_name": "user_create",
            "user_id": user.id
        })
        return user

    @staticmethod
    async def update_user_service(
            user_in: UserUpdateIn,
            token: Annotated[str, Depends(oauth2_scheme)],
            user_uow: UserUnitOfWork = Depends(get_user_uow)
    ):
        user_id = get_sub_from_token(token)
        delete_none_params(user_in)

        user = await user_uow.update_user_uow(user_in, user_id)
        if not user:
            raise UserFailedUpdateException()
        await user_kafka_producer.send_data({
            "event_name": "user_update",
            "user_id": user_id
        })
        return user

    @staticmethod
    async def delete_user_service(
            token: Annotated[str, Depends(oauth2_scheme)],
            user_uow: UserUnitOfWork = Depends(get_user_uow)
    ):
        user_id = get_sub_from_token(token)

        is_deleted = await user_uow.delete_user_uow(user_id)
        if is_deleted:
            raise UserDeletedSuccessException(user_id)
        raise UserFailedDeleteException()
