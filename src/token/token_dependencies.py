from fastapi import Depends

from ..config.database.db_helper import Session, get_db
from .token_service import TokenService


def get_token_db_service(db: Session = Depends(get_db)) -> TokenService:
    """
    Фабричная функция для создания TokenService с передачей сессии БД.
    """
    return TokenService(db)


def get_token_service() -> TokenService:
    """
    Фабричная функция для создания TokenService без передачи сессии БД.
    """
    return TokenService()
