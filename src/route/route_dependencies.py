from fastapi import Depends

from .route_service import RouteService


# def get_route_service_db(db: Session = Depends(get_db)) -> RouteService:
#     """
#     Фабричная функция для создания UserService с передачей сессии БД.
#     """
#     return RouteService(db)
