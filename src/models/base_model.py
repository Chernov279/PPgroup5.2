import datetime
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
