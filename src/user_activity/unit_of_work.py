from src.repositories.sqlalchemy_uow import SqlAlchemyUnitOfWork
from src.user.user_repository import UserRepository


class UserActivityUnitOfWork(SqlAlchemyUnitOfWork):
    def __init__(self, db_session):
        super().__init__(db_session)
        self.db_session = db_session
        self.repo = UserRepository(db_session)

    async def update_active_user_uow(self, user_id: int, **kwargs):
        try:
            await self.repo.update_user_activity(user_id, **kwargs)
            await self.db_session.commit()
        except Exception as e:
            await self.db_session.rollback()
            raise e

    async def update_user_activity_uow(self, user_id: int, is_active: bool):
        try:
            await self.repo.update_user_activity(user_id, is_active=is_active)
            await self.db_session.commit()
        except Exception as e:
            await self.db_session.rollback()
            raise e