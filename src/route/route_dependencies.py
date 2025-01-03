from fastapi import Depends

from ..config.database.db_helper import Session, get_db
from .route_service import RouteService


def get_route_service_db(db: Session = Depends(get_db)) -> RouteService:
    """
    Фабричная функция для создания UserService с передачей сессии БД.
    """
    return RouteService(db)
