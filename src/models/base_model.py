import datetime
from typing import Any, List

from sqlalchemy import TIMESTAMP, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseModel(DeclarativeBase):
    __abstract__ = True

    # created_at: Mapped[datetime.datetime] = mapped_column(default=func.now())
    # updated_at: Mapped[datetime.datetime] = mapped_column(
    #     TIMESTAMP(timezone=True),
    #     default=func.now(),
    #     onupdate=func.now()
    # )
    @classmethod
    def get_pk_columns(cls) -> List[Any]:
        return [col.name for col in cls.__table__.primary_key]

    @classmethod
    def get_column_by_name(cls, column_name) -> Any:
        return getattr(cls, column_name)

    @classmethod
    def get_columns_by_names(cls, *column_names) -> Any:
        return [getattr(cls, column_name) for column_name in column_names]
