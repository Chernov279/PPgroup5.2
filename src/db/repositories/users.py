from datetime import datetime, timedelta
from typing import Optional, List, Any, Union

from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.base import BaseSchema
from src.schemas.schemas import UserBaseSchema

from ..models.models import User
from ..repositories.sqlalchemy_repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository[User]):
    """
    Репозиторий для работы с пользователями в базе данных.

    Attributes:
        db_session (AsyncSession): Асинхронная сессия SQLAlchemy для работы с БД
        model (Type[User]): Модель пользователя для операций с БД
    """

    def __init__(self, db_session: AsyncSession) -> None:
        super().__init__(db_session, User)

    async def get_user_model_by_id(self, user_id: int) -> Optional[User]:
        """
        Получить полную модель пользователя по его уникальному идентификатору.

        Args:
            user_id (int): Идентификатор пользователя

        Returns:
            Optional[User]: Объект пользователя или None, если пользователь не найден

        """
        return await self.get_by_id(user_id)


    async def get_user_by_id(
            self,
            user_id: int,
            selected_columns: (Optional[List[Any]]) = None
    ) -> Union[User, UserBaseSchema, None]:
        """
        Получить полную с выбранными колонками пользователя по его уникальному идентификатору.

        Args:
            user_id (int): Идентификатор пользователя
            selected_columns (Optional[List[Any]]): Список столбцов для выборки.
                Если None, выбираются все столбцы, - тогда лучше использовать get_user_model_by_id

        Returns:
            Union[User, UserBaseSchema, None]: Объект пользователя, схема с выбранными столбцами пользователя
                или None, если пользователь не найден

        """
        return await self.get_single(
            User.id == user_id,
            selected_columns=selected_columns
        )


    async def get_user_by_email(
            self,
            email: str,
            selected_columns: Optional[List[Any]] = None,
    ) -> Union[User, UserBaseSchema, None]:
        """
        Получить пользователя по адресу электронной почты.

        Args:
            email (str): Адрес электронной почты пользователя
            selected_columns (Optional[List[Any]]): Список столбцов для выборки.
                Если None, выбираются все столбцы.

        Returns:
            Union[User, UserBaseSchema, None]: Объект пользователя, схема с выбранными столбцами пользователя
                или None, если пользователь не найден

        """

        return await self.get_single(
            User.email == email,
            selected_columns=selected_columns,
        )

    async def exists_user_with_email(
            self,
            email: str,
    ) -> bool:
        """
        Проверяет существование пользователя с указанным email

        Args:
            email (str): Email пользователя.

        Returns:
            bool: Существует ли пользователь
        """
        return await self.exists(User.email == email)


    async def get_all_users(
            self,
            limit: int = 100,
            offset: int = 0,
            selected_columns: Optional[List[Any]] = None
    ) -> Union[List[User], List[UserBaseSchema]]:
        """
        Получить список пользователей с пагинацией.

        Args:
            limit (int): Максимальное количество записей для возврата.
                По умолчанию 100.
            offset (int): Количество записей для пропуска.
                По умолчанию 0.
            selected_columns (Optional[List[Any]]): Список столбцов для выборки.
                Если None, выбираются все столбцы.

        Returns:
            Union[List[User], List[UserBaseSchema]]: Список объектов пользователей или схемами пользователя
        """
        return await self.get_multi(
            limit=limit,
            offset=offset,
            selected_columns=selected_columns
        )
    async def create_user(
            self,
            user_in: BaseSchema,
            returning_columns: List[Any],
        ) -> Union[User, UserBaseSchema]:
        """
        Создать нового пользователя.

        Args:
            user_in (BaseSchema): Схема с данными пользователя. Должен содержать все обязательные поля модели User
            returning_columns (List[Any]): Возвращаемые колонки созданного пользователя. Указывается обязательно
                 для предотвращения возврата чувствительных данных

        Returns:
            User: Созданный объект пользователя
        """
        return await self.create_returning(user_in, returning_columns)

    async def update_user_returning(
            self,
            user_in: BaseSchema,
            user_id: int,
            returning_columns: List[Any]
    ) -> Union[User, UserBaseSchema, None]:
        """
        Обновить данные пользователя.

        Args:
            user_in (BaseSchema): Словарь с обновляемыми данными пользователя
            user_id (int): Идентификатор пользователя для обновления
            returning_columns (List[Any]): Возвращаемые колонки обновленного пользователя. Указывается обязательно
                 для предотвращения возврата чувствительных данных

        Returns:
            Optional[User]: Обновленный объект пользователя или None,
                если пользователь не найден
        """
        return await self.update_returning(
            User.id == user_id,
            values=user_in,
            returning_columns=returning_columns
        )


    async def update_user_activity(
            self,
            last_active_time: datetime,
            user_id: int,
    ) -> bool:
        """
        Обновить статус активности пользователя.

        Args:
            last_active_time (datetime): Время последней активности пользователя
            user_id (int): Идентификатор пользователя для обновления

        Returns:
            Optional[User]: Обновленный объект пользователя или None,
                если пользователь не найден
        """
        return await self.update(
            User.id == user_id,
            values={"last_active_time": last_active_time},
        ) > 0

    async def update_threshold_activity(
            self,
            threshold: timedelta,
            user_id: int
    ):
        stmt = """
            UPDATE users 
            SET last_active_time = NOW()
            WHERE id = :user_id 
              AND (last_active_time IS NULL 
                   OR last_active_time < NOW() - :threshold)
            RETURNING id
        """

        result = await self.execute_raw(
            stmt,
            {"user_id": user_id, "threshold": threshold}
        )

        return result.rowcount > 0
    async def delete_user(self, user_id: int) -> bool:
        """
        Удалить пользователя по идентификатору.

        Args:
            user_id (int): Идентификатор пользователя для удаления

        Returns:
            bool: True, если пользователь был удален, False если пользователь не найден
        """
        return await self.delete(User.id == user_id) > 0