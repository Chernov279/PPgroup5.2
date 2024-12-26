from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from src.config.database.db_config import settings_db

Base = declarative_base()
engine = create_engine(settings_db.DATABASE_URL)
Session = sessionmaker(engine)
session = Session()


# Функция для получения сессии базы данных, которая автоматически закрывает сессию после использования
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()