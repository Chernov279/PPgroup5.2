from typing import List, Tuple, Union, Optional

from src.models.base_model import BaseModel
from src.utils.base_utils import isValidModel, hasAttrOrder, isValidSchema, isValidFilters


class BaseRepository:
    def __init__(self, db_session):
        self.db_session = db_session

    def get_single(self, model, **filters) -> Optional[BaseModel]:
        isValidModel(self, model)
        with self.db_session as session:
            obj = session.query(model).filter_by(**filters).first()
            return obj

    def get_multi(
            self,
            model,
            order: str = "id",
            limit: int = 100,
            offset: int = 0,
    ) -> List[BaseModel]:
        isValidModel(self, model)
        hasAttrOrder(model, order)

        with self.db_session as session:
            stmt = (
                session.query(model)
                .order_by(getattr(model, order))
                .limit(limit)
                .offset(offset)
            )
            return stmt.all()

    def get_multi_with_filters(
            self,
            model,
            order: str = "id",
            limit: int = 100,
            offset: int = 0,
            **filters
    ) -> List[BaseModel]:
        isValidModel(self, model)
        hasAttrOrder(model, order)
        isValidFilters(model, filters)
        with self.db_session as session:
            stmt = (
                session.query(model)
                .filter_by(**filters)
                .order_by(getattr(model, order))
                .limit(limit)
                .offset(offset)
            )
            return stmt.all()

    def create(self, model, schema, commit=True) -> BaseModel:
        isValidModel(self, model)
        isValidSchema(self, schema, model)
        data = schema.model_dump()
        with self.db_session as session:
            instance = model(**data)
            session.add(instance)
            if commit:
                session.commit()
                session.refresh(instance)
            return instance

    def void_multi_create(self, model, schemas: Union[List, Tuple], checkpoint=False, commit=True) -> None:
        isValidModel(self, model)
        with self.db_session as session:
            for schema in schemas:
                isValidSchema(self, schema, model)

                data = schema.model_dump()

                instance = model(**data)
                session.add(instance)
                if checkpoint and commit:
                    session.commit()
            if commit:
                session.commit()

    def multi_create_with_return(self, model, schemas: Union[List, Tuple], checkpoint=False, commit=True) -> List[BaseModel]:
        isValidModel(self, model)
        returning = [None] * len(schemas)

        with self.db_session as session:
            for schema_ind in range(len(schemas)):
                schema = schemas[schema_ind]
                isValidSchema(self, schema, model)

                data = schema.model_dump()

                instance = model(**data)
                session.add(instance)
                session.refresh(instance)
                returning[schema_ind] = instance

                if checkpoint and commit:
                    session.commit()
            if commit:
                session.commit()
            return returning

    def update_by_filters(self, model, schema, commit=True, **filters) -> BaseModel:
        isValidModel(self, model)
        isValidSchema(self, schema)
        isValidFilters(model, filters)

        data = schema.model_dump()
        with self.db_session as session:
            session.query(model).filter_by(**filters).update(data, synchronize_session="fetch")
            if commit:
                session.commit()
            return session.query(model).filter_by(**filters).first()

    def update_by_obj(self, obj, schema, commit=True) -> BaseModel:
        isValidModel(self, obj.__class__)
        isValidSchema(self, schema)

        data = schema.model_dump()
        with self.db_session as session:
            # obj = session.merge(obj)
            for key, value in data.items():
                setattr(obj, key, value)
            if commit:
                session.commit()
                session.refresh(obj)
            return obj

    def delete_by_obj(self, obj, commit=True) -> bool:
        isValidModel(self, obj.__class__)

        with self.db_session as session:
            session.delete(obj)
            if commit:
                session.commit()
            return True

    def delete_by_filters(self, model, commit=True, **filters) -> bool:
        isValidModel(self, model)
        isValidFilters(model, filters)

        with self.db_session as session:
            deleted_count = session.query(model).filter_by(**filters).delete(synchronize_session="fetch")
            if commit:
                session.commit()
            return deleted_count > 0
