from src.repositories.sqlalchemy_uow import SqlAlchemyUnitOfWork
from src.user.user_repository import UserRepository


class TokenUnitOfWork(SqlAlchemyUnitOfWork):
    # TODO check_login_what_is
    def __init__(self, db_session):
        super().__init__(db_session)
        self.db_session = db_session
        self.repository = UserRepository(db_session)

    async def login_by_password_uow(self, email, selected_columns):
        try:
            user = await self.repository.get_user_by_email(
                email=email,
                selected_columns=selected_columns,
            )
            return user
        except Exception as e:
            await self.db_session.rollback()
            raise e

    async def get_access_token_uow(
            self,
            user_id,
            selected_columns,
    ):
        try:
            user = await self.repository.get_user_by_id(
                user_id=user_id,
                selected_columns=selected_columns,
            )
            return user
        except Exception as e:
            await self.db_session.rollback()
            raise e
