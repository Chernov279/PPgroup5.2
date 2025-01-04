from src.config.database.db_helper import Base


class BaseModel(Base):
    __abstract__ = True
