from typing import List, Optional, Any
from sqlalchemy import func, select, delete

from .base_repository import AbstractRepository
from ..exceptions.user_exceptions import UserNotFoundException
from ..models.base_model import BaseModel
from ..utils.base_utils import isValidModel, hasAttrOrder, isValidSchema, isValidFilters


# TODO add method get_by_pk
class SQLAlchemyRepository(AbstractRepository):
    def __init__(self, db_session, model: type(BaseModel)):
        self.db_session = db_session
        isValidModel(self, model)
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
        hasAttrOrder(self.model, order)

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
    ) -> List[BaseModel]:

        hasAttrOrder(self.model, order)
        isValidFilters(self.model, filters)

        stmt_select = (select(*selected_columns).select_from(self.model if selected_columns else select(self.model)))
        stmt = (
            stmt_select
            .filter_by(**filters)
            .order_by(getattr(self.model, order))
            .limit(limit)
            .offset(offset)
        )
        result = self.db_session.execute(stmt)
        return result.all()

    async def get_max(
            self,
            column_name: str,
            limit=1,
            selected_columns: Optional[List[Any]] = None,
            **filters
    ):

        hasAttrOrder(self.model, column_name)

        subquery = select(
            (func.max(getattr(self.model, column_name))).scalar_subquery()
        )
        stmt_select = (select(*selected_columns).select_from(self.model if selected_columns else select(self.model)))
        stmt = stmt_select.where(getattr(self.model, column_name) == subquery)
        for key, value in filters.items():
            stmt = stmt.where(getattr(self.model, key) == value)
        stmt = stmt.limit(limit)
        result = await self.db_session.execute(stmt)
        return result.first()

    async def get_min(
            self,
            column_name: str,
            limit=1,
            selected_columns: Optional[List[Any]] = None,
            **filters
    ):
        hasAttrOrder(self.model, column_name)

        subquery = select(
            (func.min(getattr(self.model, column_name))).scalar_subquery()
        )
        stmt_select = (select(*selected_columns).select_from(self.model if selected_columns else select(self.model)))
        stmt = stmt_select.where(getattr(self.model, column_name) == subquery)
        for key, value in filters.items():
            stmt = stmt.where(getattr(self.model, key) == value)
        stmt = stmt.limit(limit)
        result = await self.db_session.execute(stmt)
        return result.first()

    async def create(
            self,
            schema,
            flush: bool = True,
            selected_columns: Optional[List] = None
    ) -> Optional[BaseModel]:
        isValidSchema(self, self.model, schema)

        data = schema.model_dump()

        instance = self.model(**data)
        self.db_session.add(instance)
        if flush:
            await self.db_session.flush()
            await self.db_session.refresh(instance)
            return instance

    # async def void_multi_create(self, schemas: Union[List, Tuple], checkpoint=False, commit=True) -> None:
    #
    #     async with self.db_session() as session:
    #         for schema in schemas:
    #             isValidSchema(self, self.model, schema)
    #
    #             data = schema.model_dump()
    #
    #             instance = self.model(**data)
    #             session.add(instance)
    #             if checkpoint and commit:
    #                 await session.commit()
    #         if commit:
    #             await session.commit()
    #
    # async def multi_create_with_return(self, schemas: Union[List, Tuple], checkpoint: bool = False, commit: bool = True,
    #                                    commit_step: int = 10) -> List:
    #     returning = [None] * len(schemas)
    #     cur_commit_step = 0
    #     async with self.db_session as session:
    #         for schema_ind in range(len(schemas)):
    #
    #             schema = schemas[schema_ind]
    #             isValidSchema(self, self.model, schema)
    #
    #             data = schema.model_dump()
    #
    #             instance = self.model(**data)
    #             session.add(instance)
    #             await session.refresh(instance)
    #             returning[schema_ind] = instance
    #
    #             if commit and checkpoint:
    #                 if cur_commit_step == 10 or cur_commit_step > 10:
    #                     await session.commit()
    #                     cur_commit_step = 0
    #                 else:
    #                     cur_commit_step += 1
    #         if commit:
    #             await session.commit()
    #         return returning
    #
    async def update(
            self,
            schema,
            **filters
    ) -> BaseModel:
        isValidSchema(self, self.model, schema)
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

    async def update_by_pk(
            self,
            schema,
            pk_values: List[Any],

    ) -> BaseModel:
        isValidSchema(self, self.model, schema)

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
