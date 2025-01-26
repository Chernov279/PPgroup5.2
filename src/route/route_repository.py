from typing import List

from ..config.database.db_helper import Session
from ..models.models import Route, User
from .route_schemas import RouteCreateIn, RouteUpdateIn


class RouteRepository:
    def __init__(
            self,
            db: Session
    ):
        self.db = db

    def get_user_id_by_route_id_repo(self, route_id) -> Route:
        route = self.db.query(Route).filter(Route.id == route_id).first()
        if route:
            return route.user_id

    def get_route_by_id_repo(self, route_id) -> Route:
        route = self.db.query(Route).filter(Route.id == route_id).first()
        return route

    def get_routes_repo(self) -> List[Route]:
        routes = self.db.query(Route).all()
        return routes

    def get_routes_by_user_repo(self, user: User) -> List[Route]:
        routes = self.db.query(Route).filter(Route.user == user).all()
        return routes

    def get_routes_by_user_id_repo(self, user_id: int) -> List[Route]:
        routes = self.db.query(Route).filter(Route.user_id == user_id).all()
        return routes

    def create_route_repo(self, route_in: RouteCreateIn, user_id: int) -> List[Route]:
        route = Route(
            user_id=user_id,
            distance=route_in.distance,
            users_travel_time=route_in.users_travel_time,
            users_travel_speed=route_in.users_travel_speed,
            users_transport=route_in.users_transport,
            comment=route_in.comment,
            locname_start=route_in.locname_start,
            locname_finish=route_in.locname_finish,
        )
        self.db.add(route)
        self.db.commit()
        self.db.refresh(route)
        return route

    def update_route_repo(
            self,
            route_in: RouteUpdateIn,
            route: Route
    ):
        updated = False

        if route:
            if route_in.distance and route.distance != route_in.distance:
                route.distance = route_in.distance
                updated = True

            if route_in.users_travel_time and route.users_travel_time != route_in.users_travel_time:
                route.users_travel_time = route_in.users_travel_time
                updated = True

            if route_in.users_travel_speed and route.users_travel_speed != route_in.users_travel_speed:
                route.users_travel_speed = route_in.users_travel_speed
                updated = True

            if route_in.users_transport and route.users_transport != route_in.users_transport:
                route.users_transport = route_in.users_transport
                updated = True

            if route_in.comment and route.comment != route_in.comment:
                route.comment = route_in.comment
                updated = True

            if route_in.locname_start and route.locname_start != route_in.locname_start:
                route.locname_start = route_in.locname_start
                updated = True

            if route_in.locname_finish and route.locname_finish != route_in.locname_finish:
                route.locname_finish = route_in.locname_finish
                updated = True

            if updated:
                self.db.commit()
                self.db.refresh(route)
            return route

    def delete_route_repo(self, route: Route) -> bool:
        """
        Удалить пользователя.
        """
        if route:
            self.db.delete(route)
            self.db.commit()
            return True
        return False
