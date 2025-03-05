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
        return await self.get_multi(
            order=order,
            selected_columns=selected_columns,
            limit=limit,
            offset=offset,
        )

    async def get_cords_by_route(
            self,
            selected_columns,
            route_id,
            offset,
            limit: int = 100,
            order: str = "order",
    ):
        return await self.get_multi_with_filters(
            selected_columns=selected_columns,
            order=order,
            limit=limit,
            offset=offset,
            route_id=route_id,
        )

    async def get_single_cord(
            self,
            selected_columns,
            route_id,
            order,
    ):
        return await self.get_single(
            selected_columns=selected_columns,
            route_id=route_id,
            order=order
        )

    async def get_latest_order(
            self,
            route_id,
    ):
        return await self.get_max(
            column_name="order",
            route_id=route_id,
        )

    async def get_first_order(
            self,
            selected_columns,
            route_id,
    ):
        return await self.get_min(
            selected_columns=selected_columns,
            column_name="order",
            route_id=route_id
        )

    async def add_cord(
            self,
            cord_in
    ):
        return await self.create(
            schema=cord_in,
            flush=False
        )

    async def add_cords(
            self,
            cords_in,
    ):
        return await self.multi_create(
            cords_in,
        )

    async def delete_cord(
            self,
            route_id,
            order,
    ):
        return await self.delete(
            route_id=route_id,
            order=order
        )

    async def delete_cords_by_route(
            self,
            route_id
    ):
        return await self.delete(
            route_id=route_id
        )
