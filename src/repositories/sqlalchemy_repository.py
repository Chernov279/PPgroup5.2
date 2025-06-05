from typing import List, Optional, Any, Tuple, Union
from sqlalchemy import func, select, delete

from .base_repository import AbstractRepository
from ..exceptions.user_exceptions import UserNotFoundException
from ..models.base_model import DeclarativeBaseModel
from ..utils.base_utils import is_valid_model, has_attr_order, is_valid_schema, isValidFilters


# TODO add method get_by_pk
# TODO add method get_with_join
class SQLAlchemyRepository(AbstractRepository):
    def __init__(self, db_session, model: type(DeclarativeBaseModel)):
        self.db_session = db_session
        is_valid_model(self, model)
        self.model = model

    async def get_single(
            self,
            selected_columns: Optional[List[Any]] = None,
            limit: int = 1,
            scalar: bool = False,
            **filters
    ):

        isValidFilters(self.model, filters)
        row = (
            await self.db_session.execute(
                select(*selected_columns).select_from(self.model).filter_by(**filters).limit(limit))
            if selected_columns else
            await self.db_session.execute(select(self.model).filter_by(**filters).limit(limit))
        )
        if scalar:
            return row.scalar()
        return row.first()

    async def get_multi(
            self,
            order: str = "id",
            limit: int = 100,
            offset: int = 0,
            selected_columns: Optional[List[Any]] = None,
    ):
        has_attr_order(self.model, order)

        stmt_select = (
            select(*selected_columns).select_from(self.model) if selected_columns else select(self.model))
        stmt = (
            stmt_select
            .order_by(getattr(self.model, order))
            .limit(limit)
            .offset(offset)
        )
        result = await self.db_session.execute(stmt)
        return result.all()

    async def get_multi_with_filters(
            self,
            order: str = "id",
            limit: int = 100,
            offset: int = 0,
            selected_columns: Optional[List[Any]] = None,
            **filters
    ) -> List[DeclarativeBaseModel]:

        has_attr_order(self.model, order)
        isValidFilters(self.model, filters)

        stmt_select = select(*selected_columns).select_from(self.model) if selected_columns else select(self.model)
        stmt = (
            stmt_select
            .filter_by(**filters)
            .order_by(getattr(self.model, order))
            .limit(limit)
            .offset(offset)
        )
        result = await self.db_session.execute(stmt)
        return result.all()

    async def get_max(
            self,
            column_name: str,
            scalar: bool = True,
            **filters
    ):
        has_attr_order(self.model, column_name)

        stmt = select(func.max(getattr(self.model, column_name)))

        for key, value in filters.items():
            stmt = stmt.where(getattr(self.model, key) == value)

        result = await self.db_session.execute(stmt)
        if scalar:
            return result.scalar_one_or_none()
        return result.first()

    async def get_min(
            self,
            column_name: str,
            limit=1,
            selected_columns: Optional[List[Any]] = None,
            scalar: bool = False,
            **filters
    ):
        has_attr_order(self.model, column_name)

        subquery = select(
            (func.min(getattr(self.model, column_name))).scalar_subquery()
        )
        stmt_select = (select(*selected_columns).select_from(self.model if selected_columns else select(self.model)))
        stmt = stmt_select.where(getattr(self.model, column_name) == subquery)
        for key, value in filters.items():
            stmt = stmt.where(getattr(self.model, key) == value)
        stmt = stmt.limit(limit)
        result = await self.db_session.execute(stmt)
        if scalar:
            return result.scalar()
        return result.first()

    async def get_count_by_filters(
            self,
            **filters
    ) -> int:

        isValidFilters(self.model, filters)

        stmt = select(func.count()).select_from(self.model).filter_by(**filters)
        return await self.db_session.execute(stmt)

    async def get_avg_by_filters(
            self,
            column_name: str,
            **filters
    ) -> float:
        """
        Возвращает среднее значение указанного столбца с учётом фильтров.
        """
        has_attr_order(self.model, column_name)
        isValidFilters(self.model, filters)

        stmt = select(func.avg(getattr(self.model, column_name))).select_from(self.model).filter_by(**filters)
        result = await self.db_session.execute(stmt)
        return result.scalar() or None

    async def create(
            self,
            schema,
            flush: bool = True,
            selected_columns: Optional[List] = None
    ) -> Optional[DeclarativeBaseModel]:
        is_valid_schema(self, self.model, schema)

        data = schema.model_dump()

        instance = self.model(**data)
        self.db_session.add(instance)
        if flush:
            await self.db_session.flush()
            await self.db_session.refresh(instance)
            return instance

    async def multi_create(
            self,
            schemas: Union[List, Tuple],
    ) -> None:

        for schema in schemas:
            is_valid_schema(self, self.model, schema)

            data = schema.model_dump()

            instance = self.model(**data)
            self.db_session.add(instance)

    async def update(
            self,
            schema,
            **filters
    ) -> DeclarativeBaseModel:
        is_valid_schema(self, self.model, schema)
        isValidFilters(self.model, filters)

        data = schema.model_dump()

        query = select(self.model).filter_by(**filters)
        result = await self.db_session.execute(query)
        instance = result.scalars().first()

        if instance:
            for key, value in data.items():
                setattr(instance, key, value)

            return instance
        else:
            raise UserNotFoundException()

    async def update_by_dict(
            self,
            data: dict,
            **filters
    ) -> DeclarativeBaseModel:

        isValidFilters(self.model, filters)

        query = select(self.model).filter_by(**filters)
        result = await self.db_session.execute(query)
        instance = result.scalars().first()

        if instance:
            for key, value in data.items():
                setattr(instance, key, value)

            return instance
        else:
            raise UserNotFoundException()

    # TODO update_by_object, selected_columns to instance for update
    async def update_by_pk(
            self,
            schema,
            pk_values: List[Any],

    ) -> DeclarativeBaseModel:
        is_valid_schema(self, self.model, schema)

        data = schema.model_dump()

        pk_dict = dict(zip(self.model.get_pk_columns_names(), pk_values))
        query = select(self.model).filter_by(
            **pk_dict
        )
        result = await self.db_session.execute(query)
        instance = result.scalars().first()
        if instance:
            for key, value in data.items():
                setattr(instance, key, value)
            return instance
        else:
            raise UserNotFoundException()

    async def delete(
            self,
            **filters
    ) -> bool:

        isValidFilters(self.model, filters)

        query = delete(self.model).filter_by(**filters)
        result = await self.db_session.execute(query)
        if result.rowcount > 0:
            return True
        return False

    async def delete_by_pk(
            self,
            pk_values: List[Any],
    ) -> bool:
        pk_dict = dict(zip(self.model.get_pk_columns_names(), pk_values))
        query = delete(self.model).filter_by(**pk_dict)
        result = await self.db_session.execute(query)
        if result.rowcount > 0:
            return True
        return False
