from typing import ClassVar, Any

from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    __model__: ClassVar[type | None] = None
    model_columns: ClassVar[list[Any]]

    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs):
        super().__pydantic_init_subclass__(**kwargs)

        if cls.__model__ is None:
            cls.model_columns = []
            return

        cls.model_columns = [
            getattr(cls.__model__, field_name)
            for field_name in cls.model_fields
            if hasattr(cls.__model__, field_name)
        ]
