from ..models.models import Coordinate
from ..repositories.sqlalchemy_repository import SQLAlchemyRepository


class CoordinateRepository(SQLAlchemyRepository):
    def __init__(self, db_session):
        super().__init__(db_session, Coordinate)

    async def get_all_cords(
            self,
            selected_columns,
            limit,
            offset,
            order: str = "order",
    ):
        pass

    async def get_cords_by_route(
            self,
            selected_columns,
            route_id,
            offset,
            limit: int = 100,
            order: str = "order",
    ):
        pass

    async def get_single_cord(
            self,
            selected_columns,
            route_id,
            order,
    ):
        pass

    async def get_latest_order(
            self,
            route_id,
    ):
        pass

    async def get_first_order(
            self,
            selected_columns,
            route_id,
    ):
        pass

    async def add_cord(
            self,
            cord_in
    ):
        pass

    async def add_cords(
            self,
            cords_in,
    ):
        pass

    async def delete_cord(
            self,
            route_id,
            order,
    ):
        pass

    async def delete_cords_by_route(
            self,
            route_id
    ):
        pass
