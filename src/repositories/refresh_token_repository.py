from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from src.authentication.schemas import RefreshTokenInternal
from src.models.models import RefreshToken
from src.repositories.sqlalchemy_repository import SQLAlchemyRepository


class TokenRepository(SQLAlchemyRepository[RefreshToken]):
    """
    Репозиторий для работы с Токенами в базе данных.

    Attributes:
        db_session (AsyncSession): Асинхронная сессия SQLAlchemy для работы с БД
        model (Type[RefreshToken]): Модель токенов для операций с БД
    """

    def __init__(self, db_session: AsyncSession) -> None:
        super().__init__(db_session, RefreshToken)

    async def create_refresh_token(
            self,
            token_data: RefreshTokenInternal
    ) -> bool:
        """
        Создать новый refresh-токен для пользователя.

        Args:
            token_data (RefreshTokenInternal): Информация о токене для его создания

        Returns:
            RefreshToken: Созданный объект refresh-токена

        """

        return await self.create(token_data) > 0

    async def get_token_by_hash(
            self,
            token_hash: str,
            scalar: bool = False
    ) -> RefreshToken:
        """
        Вернуть токен по его хэшу

        Args:
            token_hash (str): Хэш токена
            scalar (bool): Получить скалярное значение или нет

        Returns:
            RefreshToken: Объект refresh-токена

        """
        return await self.get_single(
            RefreshToken.token_hash == token_hash,
            scalar=scalar,
        )

    async def revoke_tokens_by_user_id(self, user_id: int) -> bool:
        return await self.update(
            RefreshToken.user_id == user_id,
            values={
                "revoked_at": datetime.now(timezone.utc),
            },
        ) > 0


    async def revoke_token(self, token_id: int) -> bool:
        return await self.update(
            RefreshToken.id == token_id,
            values={
                "revoked_at": datetime.now(timezone.utc),
            },
        ) > 0

    async def revoke_token_by_hash(self, token_hash: str) -> bool:
        return await self.update(
            RefreshToken.token_hash == token_hash,
            values={
                "revoked_at": datetime.now(timezone.utc),
            },
        ) > 0
