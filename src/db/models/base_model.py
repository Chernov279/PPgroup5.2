from datetime import datetime
from typing import Any, List, Optional

from sqlalchemy import TIMESTAMP, MetaData, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

class DeclarativeBaseModel(DeclarativeBase):
    """Базовая модель в базе данных с общими методами."""
    __abstract__ = True
    metadata = MetaData(naming_convention=NAMING_CONVENTION)

    def __repr__(self) -> str:
        pk_values = {
            col: getattr(self, col, None)
            for col in self.get_pk_columns_names()
        }
        return f"<{self.__class__.__name__} {pk_values}>"
    
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
    created_at: Mapped[Optional[datetime]] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=True,
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=True,
    )

class PrimaryId:
    """Наследуемая базовая модель с уникальным идентификатором"""
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )
