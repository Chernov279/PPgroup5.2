from ..config.database.db_helper import Session
from ..exceptions.route_exceptions import RouteNotFoundException, RouteFailedActionException
from ..exceptions.user_exceptions import UserHasNotPermission
from src.unit_of_work.route_uow import RouteUOW
from .route_schemas import RouteCreateIn, RouteUpdateIn, RouteDetailOut
from .route_repository import RouteRepository


class RouteService:
    def __init__(
            self,
            db: Session = None
    ):
        if db:
            self.route_uow = RouteUOW(db)
            self.route_repo = RouteRepository(db)

    def get_route_by_id_service(self, route_id: int):
        route = self.route_repo.get_route_by_id_repo(route_id)
        if route:
            return route
        raise RouteNotFoundException(route_id)

    def get_routes_service(self):
        routes = self.route_repo.get_routes_repo()
        return routes

    def get_route_detail_service(
            self,
            route_id: int,
            token: str
    ):
        route = self.route_repo.get_route_by_id_repo(route_id)
        if not route:
            raise RouteNotFoundException(route_id)
        user_name = route.user.name

        args_estimation = self.route_uow.get_avg_estimation_by_route_uow(route)
        if args_estimation is not None:
            amount_estimations, avg_estimation = args_estimation
        else:
            amount_estimations, avg_estimation = 0, None

        args_coordinates = self.route_uow.get_sf_coordinates_by_route_uow(route)
        if args_coordinates is not None:
            amount_points, start_coordinate, finish_coordinate = args_coordinates
        else:
            amount_points, start_coordinate, finish_coordinate = 0, None, None

        route_detail_out = RouteDetailOut(
            id=route_id,
            distance=route.distance,
            users_travel_time=route.users_travel_time,
            users_travel_speed=route.users_travel_speed,
            users_transport=route.users_transport,
            comment=route.comment,
            created_time=route.created_time,
            locname_start=route.locname_start,
            locname_finish=route.locname_finish,
            user_name=user_name,
            avg_estimation=avg_estimation,
            amount_estimations=amount_estimations,
            start_coordinate=start_coordinate,
            finish_coordinate=finish_coordinate,
            amount_points=amount_points,
        )
        return route_detail_out

    def create_route_service(
            self,
            route_in: RouteCreateIn,
            token: str
    ):
        user_id = self.route_uow.get_user_id_by_token_uow(token)
        if not user_id:
            raise
        return self.route_repo.create_route_repo(route_in, user_id)

    def get_my_routes_service(
            self,
            token: str
    ):
        routes = self.route_uow.get_routes_by_token_uow(token)
        return routes

    def update_route_service(
            self,
            route_in: RouteUpdateIn,
            token: str
    ):
        route_id = route_in.id
        route = self.route_repo.get_route_by_id_repo(route_id)
        if not route:
            raise RouteNotFoundException(route_id)
        user_id_route = route.user_id
        user_id_token = self.route_uow.get_user_id_by_token_uow(token)
        if user_id_route != user_id_token:
            raise UserHasNotPermission(action="update route")
        updated_route = self.route_repo.update_route_repo(route_in, route)
        if updated_route:
            return updated_route
        raise RouteFailedActionException(action="update route")

    def delete_route_service(
            self,
            route_id: int,
            token: str
    ):
        route = self.route_repo.get_route_by_id_repo(route_id)
        if not route:
            raise RouteNotFoundException(route_id)
        user_id_route = route.user_id
        user_id_token = self.route_uow.get_user_id_by_token_uow(token)
        if user_id_route != user_id_token:
            raise UserHasNotPermission(action="delete route")
        success = self.route_repo.delete_route_repo(route)
        if success:
            return {"message": "Route successfully deleted"}
        raise RouteFailedActionException(action="delete route")
