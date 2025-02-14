from src.exceptions.auth_exceptions import EmailAlreadyExistsException
from src.models.models import User
from src.repositories.sqlalchemy_uow import SqlAlchemyUnitOfWork
from src.user.user_repository import UserRepository


class AuthUnitOfWork(SqlAlchemyUnitOfWork):
    def __init__(self, db_session):
        super().__init__(db_session)
        self.db_session = db_session
        self.repository = UserRepository(db_session)

    async def register_user_uow(
            self,
            auth_in
    ):
        try:
            existing_user = await self.repository.get_user_by_email(
                email=auth_in.email,
                selected_columns=User.get_pk_columns()
            )
            if existing_user:
                raise EmailAlreadyExistsException()

            user = await self.repository.register_new_user(user_in=auth_in)
            await self.db_session.commit()
            return user
        except Exception as e:
            await self.db_session.rollback()
            raise e

    async def login_user_uow(
            self,
            email,
            selected_columns
    ):
        try:
            user_data = await self.repository.get_user_by_email(
                email=email,
                selected_columns=selected_columns,
            )
            return user_data
        except Exception as e:
            raise e
