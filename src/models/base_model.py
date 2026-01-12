import datetime
from typing import Any, List

from sqlalchemy import TIMESTAMP, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class DeclarativeBaseModel(DeclarativeBase):
    """Базовая модель в базе данных с общими методами."""
    __abstract__ = True

    @classmethod
    def get_pk_columns_names(cls) -> List[str]:
        """Получает имена всех первичных ключей модели."""
        return [key.name for key in cls.__mapper__.primary_key]

    @classmethod
    def get_pk_columns(cls) -> List[Any]:
        """
        Получает объекты колонок, являющихся первичными ключами модели.
        Обычно используется для выбора конкретных колонок в базе данных через model_columns
        User.get_pk_columns() -> [User.id,]
        """
        pk_column_names = [col.name for col in cls.__mapper__.primary_key]
        return [getattr(cls, column_name) for column_name in pk_column_names]

    @classmethod
    def get_columns_by_names(cls, *column_names) -> List[Any]:
        """Получает объекты колонок по их именам.
        Обычно используется для выбора конкретных колонок в базе данных через model_columns
        User.get_columns_by_names("name", "surname", "email") -> [User.name, User.surname, User.email]
        """
        return [getattr(cls, column_name) for column_name in column_names]


class TimeBaseModel:
    """Наследуемая базовая модель с временными метками о создании и последнем обновлении."""
    created_at: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=func.now(), nullable=True
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=func.now(), onupdate=func.now(), nullable=True
    )


class PrimaryId:
    """Наследуемая базовая модель с уникальным идентификатором"""
    id: Mapped[int] = mapped_column(primary_key=True, unique=True, nullable=False, autoincrement=True)
