import logging
from datetime import timedelta, datetime, timezone
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from .repository import UserRepository
from .schemas import (
    UserUpdateIn,
    UserDetailOut,
    UserShortOut,
    UserActivityInternal,
    UserActivityOut, UserUpdateActivityOut
)
from .utils import format_user_activity
from ..exceptions.base_exceptions import FailedActionException, NoContentResponse

from ..exceptions.user_exceptions import (
    UserNotFoundException,
    UserFailedDeleteException
)
from ..schemas.database_params_schemas import MultiGetParams
from ..utils.schema_utils import add_internal_params

logger = logging.getLogger(__name__)


class UserService:
    def __init__(
            self,
            db_session: AsyncSession,
    ):
        self._db_session = db_session
        self._repo = UserRepository(db_session)

    INACTIVITY_THRESHOLD = timedelta(minutes=5)  # Время, после которого пользователь считается оффлайн
    INACTIVITY_UPDATE_THRESHOLD = timedelta(
        minutes=1
    )  # Время, после которого может происходить обновление активности пользователя


    async def get_all_users(
            self,
            token_sub: Optional[int],
            multi_get_params: MultiGetParams,
    ):
        logger.info("Incoming request to get_all_users sub=%s", token_sub)

        users = await self._repo.get_all_users(
            **multi_get_params.model_dump(),
            selected_columns=UserShortOut.model_columns
        )

        return users

    async def get_user_me(
            self,
            token_sub: int,
    ) -> UserDetailOut:

        logger.info("Incoming request to get_user_me sub=%s", token_sub)

        user = await self._repo.get_user_by_id(
            user_id=token_sub,
            selected_columns=UserDetailOut.model_columns
        )

        if not user:
            raise UserNotFoundException(token_sub)

        return user

    async def get_user_activity(
            self,
            token_sub: Optional[int],
            user_id: int
    ) -> UserActivityOut:
        logger.info("Incoming request to get_user_activity sub=%s", token_sub)

        user_activity = await self._repo.get_user_by_id(
            user_id=user_id,
            selected_columns=UserActivityInternal.model_columns
        )
        if not user_activity:
            raise UserNotFoundException()

        # is_need_change_activity: bool = check_user_activity(user_activity)

        user_activity_out = add_internal_params(
            UserActivityOut,
            user_activity,
            formatted_last_active_time=format_user_activity(user_activity.last_active_time),
        )
        return user_activity_out


    async def get_user_by_id(
            self,
            token_sub: Optional[int],
            user_id: int,
    ) -> UserDetailOut:

        logger.info("Incoming request to get_user_by_id sub=%s", token_sub)

        user = await self._repo.get_user_by_id(
            user_id,
            UserDetailOut.model_columns
        )

        if not user:
            raise UserNotFoundException(user_id)
        return user


    async def update_user(
            self,
            user_in: UserUpdateIn,
            token_sub: int
    ) -> UserDetailOut:

        logger.info("Incoming request to update_user sub=%s", token_sub)

        user = await self._repo.update_user_returning(
            user_in=user_in,
            user_id=token_sub,
            returning_columns=UserDetailOut.model_columns
        )

        if not user:
            raise UserNotFoundException()
        await self._db_session.commit()

        return user


    async def update_user_time_activity(
            self,
            token_sub: Optional[int],
            user_id: int,
            hard: bool
    ) -> None:
        logger.info("Incoming request to update_user_time_activity sub=%s", token_sub)

        is_updated: bool = False
        if hard:
            is_updated = await self._repo.update_user_activity(
                datetime.now(timezone.utc),
                user_id
            )
        else:
            is_updated = await self._repo.update_threshold_activity(
                self.INACTIVITY_UPDATE_THRESHOLD,
                user_id
            )
        if not is_updated:
            raise FailedActionException("update user activity")
        return

    async def delete_user(
            self,
            token_sub: int,
    ) -> None:

        logger.info("Incoming request to delete_user sub=%s", token_sub)

        is_deleted = await self._repo.delete_user(token_sub)
        if not is_deleted:
            raise UserFailedDeleteException()

