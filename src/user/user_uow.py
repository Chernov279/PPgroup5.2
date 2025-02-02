from src.repositories.sqlalchemy_uow import SqlAlchemyUnitOfWork
from src.user.user_repository import UserRepository


class UserUnitOfWork(SqlAlchemyUnitOfWork):
    def __init__(self, db_session):
        super().__init__(db_session)
        self.db_session = db_session
        self.repository = UserRepository(db_session)

    async def create_user_uow(self, user_in):
        try:
            user = await self.repository.create_user(user_in)
            await self.db_session.commit()
            return user
        except Exception as e:
            await self.db_session.rollback()
            raise e

    async def update_user_uow(self, user_in):
        try:
            user = await self.repository.update_user(user_in)
            await self.db_session.commit()
            return user
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
