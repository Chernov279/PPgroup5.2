from ..models.models import User
from ..repositories.sqlalchemy_repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    def __init__(self, db_session):
        super().__init__(db_session, User)

    async def get_user_by_id(self, user_id, selected_columns):
        """
        Получить пользователя по ID.
        """
        return await self.get_single(
            id=user_id,
            selected_columns=selected_columns
        )

    async def get_user_by_email(self, email, selected_columns):
        """
        Получить пользователя по email.
        """
        return await self.get_single(
            email=email,
            selected_columns=selected_columns
        )

    async def get_all_users(self, limit, offset, selected_columns):
        return await self.get_multi(
            limit=limit,
            offset=offset,
            selected_columns=selected_columns
        )

    async def get_user_id_by_data(self, email):
        return await self.get_single(
            email=email,
        )

    async def get_user_id_password_by_login(self, selected_columns, email):
        return await self.get_single(
            selected_columns=selected_columns,
            email=email,
        )

    async def create_user(self, user_in):
        return await self.create(
            user_in
        )

    async def update_user(self, user_in, user_id):
        return await self.update_by_pk(
            schema=user_in,
            pk_values=[user_id,],
        )

    async def delete_user(self, user_id):
        return await self.delete_by_pk(
            pk_values=[user_id,]
        )
