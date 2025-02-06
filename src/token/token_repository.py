from ..models.models import User
from ..repositories.sqlalchemy_repository import SQLAlchemyRepository


class TokenRepository(SQLAlchemyRepository):
    def __init__(self, db_session):
        super().__init__(db_session, User)

    async def get_user_id_by_data(self, email):
        return await self.get_single(
            email=email,
        )

    async def get_user_id_password_by_login(self, selected_columns, email):
        return await self.get_single(
            selected_columns=selected_columns,
            email=email,
        )
