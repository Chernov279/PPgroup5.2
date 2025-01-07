from typing import Tuple

from src.config.database.db_helper import Session
from src.models.models import Route
from src.route.route_repository import RouteRepository
from src.token.token_repository import TokenRepository
from src.user.user_repository import UserRepository


class RouteUOW:
    def __init__(
            self,
            db: Session = None,
    ):
        self.db = db
        if db:
            self.user_repository = UserRepository(db)
            self.token_repository = TokenRepository(db)
        else:
            self.user_repository = UserRepository()
            self.token_repository = TokenRepository()

    def get_routes_by_token_uow(self, token):
        user_id = self.token_repository.get_user_id_by_token_rep(token)
        if user_id:
            routes = self.user_repository.get_user_by_id(user_id).routes
            return routes

    def get_user_id_by_token_uow(self, token):
        user_id = self.token_repository.get_user_id_by_token_rep(token)
        return user_id

    def is_route_exists_uow(self, route_id: int) -> bool:
        route_repo = RouteRepository(self.db)
        route = route_repo.get_route_by_id_repo(route_id)
        if route:
            return True
        return False

    @staticmethod
    def get_avg_estimation_by_route_uow(route: Route) -> Tuple[int, float] | None:
        estimations = route.estimations
        amount_estimations = len(estimations)
        if amount_estimations:
            avg_estimation = round(sum(map(lambda x: x.value, estimations)) / amount_estimations, 2)
            return amount_estimations, avg_estimation
        return None

    @staticmethod
    def get_sf_coordinates_by_route_uow(
            route: Route
    ) -> Tuple[int, Tuple[float, float], Tuple[float, float]] | None:
        coordinates = sorted(route.coordinates, key=lambda x: x.created_time)
        if coordinates:
            start_coordinate_obj = coordinates[0]
            finish_coordinate_obj = coordinates[-1]
            start_coordinate = (start_coordinate_obj.latitude, start_coordinate_obj.longitude,)
            finish_coordinate = (finish_coordinate_obj.latitude, finish_coordinate_obj.longitude,)

            amount_points = len(coordinates)
            return amount_points, start_coordinate, finish_coordinate

    @staticmethod
    def get_user_id_route_uow(
            route: Route
    ) -> Tuple[int, float] | None:
        estimations = route.estimations
        amount_estimations = len(estimations)
        if amount_estimations:
            avg_estimation = round(sum(map(lambda x: x.value, estimations)) / amount_estimations, 2)
            return amount_estimations, avg_estimation
        return None