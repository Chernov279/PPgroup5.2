from ..models.models import Coordinate
from ..repositories.base_repositories import BaseRepository


class CoordinateRepository(BaseRepository):
    def __init__(
            self,
            db_session
    ):
        super().__init__(db_session)

    def get_all_cords(
            self,
    ):
        return self.get_multi(
            Coordinate,
            order="route_id",
        )

    def get_cords_by_route_id(
            self,
            route_id,
            offset,
            limit: int = 100
    ):
        return self.get_multi_with_filters(
            Coordinate,
            order="order",
            limit=limit,
            offset=offset,
            route_id=route_id,
        )

    def get_single_cord(
            self,
            route_id,
            order,
    ):
        return self.get_single(
            Coordinate,
            route_id=route_id,
            order=order
        )

    def get_latest_order(
            self,
            route_id
    ):
        return self.get_max(
            model=Coordinate,
            name="order",
            route_id=route_id
        )

    def get_first_order(
            self,
            route_id
    ):
        return self.get_min(
            model=Coordinate,
            name="order",
            route_id=route_id
        )

    def add_cord(
            self,
            cord_in
    ):
        return self.create(
            Coordinate,
            cord_in
        )

    def add_cords(
            self,
            cords,
    ):
        return self.void_multi_create(
            Coordinate,
            cords
        )

    def delete_cords(
            self,
            route_id
    ):
        return self.delete_by_filters(
            Coordinate,
            route_id=route_id
        )
