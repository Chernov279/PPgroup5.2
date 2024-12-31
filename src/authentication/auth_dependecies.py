from fastapi import Depends
from sqlalchemy.orm import Session

from .auth_service import UserAuthService
from src.config.database.db_helper import get_db


def get_user_auth_service_db(db: Session = Depends(get_db)) -> UserAuthService:
    """
    Фабричная функция для создания UserService с передачей сессии БД.
    """
    return UserAuthService(db)


def get_user_auth_service() -> UserAuthService:
    """
    Фабричная функция для создания UserService без передачи сессии БД.
    """
    return UserAuthService()
