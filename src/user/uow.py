from typing import List, Optional

from .repository import UserRepository

from ..exceptions.user_exceptions import UserNotFoundException
from ..repositories.sqlalchemy_uow import SqlAlchemyUnitOfWork


class UserUnitOfWork(SqlAlchemyUnitOfWork):
    def __init__(self, db_session):
        super().__init__(db_session)
        self.db_session = db_session
        self.repository = UserRepository(db_session)

    async def get_all_users_uow(
        self,
        limit: int = 30,
        offset: int = 0,
        selected_columns: Optional[List] = None
    ):
        try:
            users = await self.repository.get_all_users(
                limit=limit,
                offset=offset,
                selected_columns=selected_columns,
            )
            return users
        except Exception as e:
            raise e

    async def get_user_by_id_uow(
            self,
            user_id: int,
            selected_columns: Optional[List] = None
    ):
        try:
            user = await self.repository.get_user_model_by_id(user_id=user_id)
            return user
        except Exception as e:
            raise e

    async def create_user_uow(self, user_in):
        try:
            user = await self.repository.create_user_returning(user_in)
            await self.db_session.commit()
            return user
        except Exception as e:
            await self.db_session.rollback()
            raise e

    async def update_user_uow(self, user_in, user_id):
        try:
            user = await self.repository.update_user_returning(user_in, user_id, )
            await self.db_session.commit()
            return user
        except UserNotFoundException:
            await self.db_session.rollback()
            raise UserNotFoundException(user_id)
        except Exception as e:
            await self.db_session.rollback()
            raise e

    async def delete_user_uow(self, user_id):
        try:
            is_deleted = await self.repository.delete_user(user_id)
            await self.db_session.commit()
            return is_deleted
        except Exception as e:
            await self.db_session.rollback()
            raise e
