from typing import List, Optional, Any, TypeVar, Dict, Generic, Union
from sqlalchemy import func, select, delete, BinaryExpression, insert, update

from .base_repository import AbstractRepository
from ..exceptions.repository_exceptions import NotFoundException
from ..models.base_model import DeclarativeBaseModel
from ..schemas.base_schemas import BaseSchema

T = TypeVar('T', bound=DeclarativeBaseModel)
S = TypeVar('S', bound=BaseSchema)


class SQLAlchemyRepository(AbstractRepository, Generic[T]):
    def __init__(self, db_session, model: type[T]):
        self.db_session = db_session
        self.model = model


    async def get_by_id(self, id: int) -> Optional[T]:
        """Возвращает объект по id"""
        result = await self.db_session.get(self.model, id)
        return result


    async def get_single(
            self,
            *filters: BinaryExpression,
            selected_columns: Optional[List[Any]] = None,
            options: Optional[List] = None,
            scalar: bool = False,
    ) -> Optional[T]:
        """
        Получить одну запись.

        Args:
            selected_columns: Список колонок для выбора [User.id, User.email]
            options: SQLAlchemy options для eager loading
            scalar: Получение всего объекта или первого столбца
            *filters: Условия WHERE (User.age > 18, User.name == "John")

        Returns:
            Row-объект если model_columns указан, иначе объект модели
        """
        if selected_columns:
            stmt = select(*selected_columns).select_from(self.model).where(*filters)
        else:
            stmt = select(self.model).where(*filters)

        if options:
            stmt = stmt.options(*options)
        stmt = await self.db_session.execute(stmt)
        if scalar:
            return stmt.scalar_one_or_none()
        return stmt.first()


    async def get_multi(
            self,
            *filters: BinaryExpression,
            selected_columns: Optional[List[Any]] = None,
            limit: int = 30,
            offset: int = 0,
            order: Optional[Any] = None,
            options: Optional[List] = None,
            scalar: bool = False,
    ) -> List[Any]:
        """
        Получить несколько записей с пагинацией.

        Args:
            *filters: Условия WHERE
            selected_columns: Список колонок
            limit: Максимальное количество записей
            offset: Смещение
            order: Поле для сортировки (User.email)
            options: Options для eager loading
            scalar: Получение всех моделей или первых столбцов

        Returns:
            Список Row-объектов если model_columns указан, иначе список моделей
        """
        stmt_select = (
            select(*selected_columns).select_from(self.model) if selected_columns else select(self.model))
        stmt = (
            stmt_select
            .order_by(order)
            .limit(limit)
            .offset(offset)
            .where(*filters)
        )
        if options:
            stmt = stmt.options(*options)
        stmt = await self.db_session.execute(stmt)

        if scalar:
            return stmt.scalars()
        return stmt.all()


    async def get_max(
            self,
            *filters,
            column: Any,
    ) -> Optional[int]:
        """
        Возвращает максимальное значение указанного столбца с учетом фильтров.

        Args:
            column: Колонка модели для вычисления максимума.
            *filters: Условия WHERE для фильтрации записей.

        Returns:
            Максимальное значение или None, если нет записей.
        """
        stmt = select(func.max(column)).select_from(self.model).where(*filters)
        stmt = await self.db_session.execute(stmt)

        return stmt.scalar_one_or_none()


    async def get_min(
            self,
            *filters,
            column: Any,
    ) -> Optional[int]:
        """
        Возвращает минимальное значение указанного столбца с учетом фильтров.

        Args:
            column: Колонка модели для вычисления минимума.
            *filters: Условия WHERE для фильтрации записей.

        Returns:
            Минимальное значение или None, если нет записей.
        """
        stmt = select(func.min(column)).select_from(self.model).where(*filters)
        stmt = await self.db_session.execute(stmt)

        return stmt.scalar_one_or_none()


    async def get_count(
            self,
            *filters
    ) -> int:
        """
        Возвращает количество указанных столбцов с учетом фильтров.

        Args:
            *filters: Условия WHERE для фильтрации записей.

        Returns:
            Количество записей.
         """
        stmt = select(func.count()).select_from(self.model).where(*filters)
        stmt = await self.db_session.execute(stmt)
        return stmt.scalar()


    async def get_avg(
            self,
            *filters,
            column: Any,
    ) -> Optional[float]:
        """
        Возвращает среднее значение указанного столбца с учетом фильтров.

        Args:
            column: Колонка модели для вычисления среднего.
            *filters: Условия WHERE для фильтрации записей.

        Returns:
            Среднее значение (float) или None, если нет записей.
        """
        stmt = select(func.avg(column)).select_from(self.model).where(*filters)
        result = await self.db_session.execute(stmt)
        return result.scalar_one_or_none()


    async def exists(self, *filters: Any) -> bool:
        """
        Проверяет существование хотя бы одной записи, соответствующей фильтрам.

        Args:
            *filters: Условия WHERE для фильтрации записей.

        Returns:
            True, если существует хотя бы одна запись, иначе False.
        """
        stmt = select(func.count()).select_from(self.model).where(*filters)
        result = await self.db_session.execute(stmt)
        count = result.scalar()
        return count > 0


    async def create(
            self,
            values: Union[Dict[str, Any], BaseSchema],
    ) -> int:
        """
        Создать новый объект в БД.

        Args:
            values: Словарь {поле: значение} или схема

        Returns:
            Количество созданных записей
        """
        if not values:
            return 0
        if isinstance(values, BaseSchema):
            values = values.model_dump()

        stmt = insert(self.model).values(values)
        result = await self.db_session.execute(stmt)

        return result.rowcount


    async def create_orm(
            self,
            schema: S,
            flush: bool = True
    ) -> T:
        """
        Создать одну запись с помощью ORM (add).

        Args:
            schema: Pydantic схема
            flush: Автоматически флашить сессию, чтобы вернуть обновленную информацию из БД

        Returns:
            Созданный объект
        """
        data = schema.model_dump(exclude_unset=True)
        instance = self.model(**data)

        self.db_session.add(instance)

        if flush:
            await self.db_session.flush()
            await self.db_session.refresh(instance)

        return instance


    async def create_returning(
            self,
            values: Union[Dict[str, Any], BaseSchema],
            returning_columns: Optional[List]= None
    ) -> Optional[Any]:
        """
        Создать объект с возвратом обновленных столбцов.

        Args:
            values: Словарь {поле: значение} или схема
            returning_columns: Возвращаемые колонки после создания.
                Если None, возвращается вся модель - осторожно для моделей с чувствительными данными

        Returns:
            Optional[Any]: запрошенные колонки или вся модель. None если нет values или ничего не обновилось
        """
        if not values:
            return None
        if isinstance(values, BaseSchema):
            values = values.model_dump()

        is_returning: bool = bool(returning_columns)

        stmt = insert(self.model).values(values)
        if is_returning:
            stmt = stmt.returning(*returning_columns)
        else:
            stmt = stmt.returning()
        result = await self.db_session.execute(stmt)

        return result.one_or_none()


    async def update(
            self,
            *filters: BinaryExpression,
            values: Union[Dict[str, Any], BaseSchema],
    ) -> int:
        """
        Обновить объект в БД по полученным данным, заменив старые значения на новые для подходящих колонок.

        Args:
            *filters: Условия WHERE
            values: Словарь {поле: значение} или схема

        Returns:
            Количество обновленных записей
        """
        if not values:
            return 0
        if isinstance(values, BaseSchema):
            values = values.model_dump()

        stmt = update(self.model).values(values).where(*filters)
        result = await self.db_session.execute(stmt)

        return result.rowcount


    async def update_orm(
            self,
            *filters: BinaryExpression,
            schema: S,
            flush: bool = True,
    ) -> Optional[T]:
        """
        Обновить одну запись через ORM. Приходящие None значения в БД также будут изменены на null

        Args:
            schema: Pydantic схема с обновляемыми полями
            *filters: Условия WHERE для выбора записи
            flush: Автоматически флашить сессию

        Returns:
            Обновленный объект или None если не найден
        """
        data = schema.model_dump(exclude_unset=True)

        if not data:
            return None

        stmt = select(self.model).where(*filters)
        result = await self.db_session.execute(stmt)
        instance = result.scalar_one_or_none()

        if not instance:
            raise NotFoundException(self.model)

        for key, value in data.items():
            setattr(instance, key, value)

        if flush:
            await self.db_session.flush()
            await self.db_session.refresh(instance)

        return instance


    async def update_returning(
            self,
            *filters: BinaryExpression,
            values: Union[Dict[str, Any], BaseSchema],
            returning_columns: Optional[List ]= None
    ) -> Optional[Any]:
        """
        Обновить объект с возвратом обновленных колонок.

        Args:
            *filters: Условия WHERE
            values: Словарь {поле: значение} или схема
            returning_columns: Возвращаемые колонки после обновления.
                Если None, возвращается вся модель - осторожно для моделей с чувствительными данными

        Returns:
            Optional[Any]: запрошенные колонки или вся модель. None если нет values или ничего не обновилось
        """
        if not values:
            return None
        if isinstance(values, BaseSchema):
            values = values.model_dump()

        is_returning: bool = bool(returning_columns)

        stmt = update(self.model).values(values).where(*filters)
        if is_returning:
            stmt = stmt.returning(*returning_columns)
        else:
            stmt = stmt.returning()
        result = await self.db_session.execute(stmt)

        return result.one_or_none()


    async def delete(
        self,
        *filters: BinaryExpression,
    ) -> int:
        """
        Удаляет записи, соответствующие фильтрам.

        Args:
            *filters: Условия WHERE для фильтрации записей.

        Returns:
            int: количество удаленных записей
        """
        stmt = delete(self.model).where(*filters)
        result = await self.db_session.execute(stmt)
        return result.rowcount


    async def execute_raw(self, query: str, params: Optional[Dict] = None) -> Any:
        """
        Выполнить сырой SQL запрос.

        Args:
            query: SQL запрос
            params: Параметры для запроса

        Returns:
            Результат выполнения
        """
        if params:
            result = await self.db_session.execute(query, params)
        else:
            result = await self.db_session.execute(query)
        return result