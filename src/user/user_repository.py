from ..models.models import User
from ..repositories.sqlalchemy_repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    def __init__(self, db_session):
        super().__init__(db_session, User)

    async def get_user_by_id(self, user_id: int, selected_columns):
        """
        Получить пользователя по ID.
        """
        return await self.get_single(id=user_id, selected_columns=selected_columns)

    async def get_user_by_email(self, email: str, selected_columns):
        """
        Получить пользователя по email.
        """
        return await self.get_single(email=email, selected_columns=selected_columns)

    async def get_all_users(self, limit, offset, selected_columns):
        return await self.get_multi(limit=limit, offset=offset, selected_columns=selected_columns)

    async def create_user(self, user_in):
        return await self.create(
            user_in
        )

    async def update_user(self, user_in, selected_columns):
        return await self.update(
            schema=user_in,
            selected_columns=selected_columns,
            id=user_in.user_id
        )

    async def delete_user(self, user_id):
        return await self.delete(id=user_id)

