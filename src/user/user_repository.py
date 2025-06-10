from ..models.models import User
from ..repositories.sqlalchemy_repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    def __init__(self, db_session):
        super().__init__(db_session, User)

    async def get_user_by_id(self, user_id, selected_columns, scalar=False):
        """
        Получить пользователя по ID.
        """
        return await self.get_single(
            selected_columns=selected_columns,
            scalar=scalar,
            id=user_id,
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

    async def create_user(self, user_in):
        return await self.create(
            user_in
        )

    async def register_new_user(self, user_in):
        return await self.create(
            schema=user_in,
            flush=True,
        )

    async def update_user(self, user_in, user_id):
        return await self.update_by_pk(
            schema=user_in,
            pk_values=[user_id,],
        )

    async def update_user_activity(self, user_id: int, **kwargs):
        return await self.update_by_dict(
            kwargs,
            id=user_id
        )

    async def delete_user(self, user_id):
        return await self.delete_by_pk(
            pk_values=[user_id,]
        )
