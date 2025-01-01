from fastapi import Depends
from sqlalchemy.orm import Session

from ..config.database.db_helper import get_db
from .user_service import UserService


def get_user_service_db(db: Session = Depends(get_db)) -> UserService:
    """
    Фабричная функция для создания UserService с передачей сессии БД.
    """
    return UserService(db)


def get_user_service() -> UserService:
    """
    Фабричная функция для создания UserService без передачи сессии БД.
    """
    return UserService()
