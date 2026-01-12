from typing import ClassVar, Any

from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    __model__: ClassVar[type | None] = None
    model_columns: ClassVar[list[Any]]

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        if cls.__model__ is None:
            return

        cls.model_columns = [
            getattr(cls.__model__, field)
            for field in cls.model_fields
            if hasattr(cls.__model__, field)
        ]
