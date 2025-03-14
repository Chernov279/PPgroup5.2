from typing import List, Optional

from ..models.models import Route

from ..repositories.sqlalchemy_repository import SQLAlchemyRepository


class RouteRepository(SQLAlchemyRepository):
    def __init__(self, db_session):
        super().__init__(db_session, Route)

    # async def get_user_id_by_route_id_repo(self, route_id) -> Route:
    #     route = self.db.query(Route).filter(Route.id == route_id).first()
    #     if route:
    #         return route.user_id

    async def get_route_by_id(
            self,
            route_id,
            selected_columns: Optional[List] = None,
            scalar: bool = False,
            limit: int = 1,
    ):
        return await self.get_single(
            selected_columns=selected_columns,
            id=route_id,
            scalar=scalar,
            limit=limit,
        )

    async def get_all_routes(
            self,
            limit,
            offset,
            selected_columns,
    ):
        return await self.get_multi(
            limit=limit,
            offset=offset,
            selected_columns=selected_columns,
        )

    async def get_routes_by_user_id(
            self,
            user_id,
            limit,
            offset,
            selected_columns,
    ):
        return await self.get_multi_with_filters(
            limit=limit,
            offset=offset,
            selected_columns=selected_columns,
            user_id=user_id,
        )

    async def create_route(
            self,
            route_in,
            flush=True
    ):
        return await self.create(
            schema=route_in,
            flush=flush
        )

    async def update_route(
            self,
            route_in,
            pk_values,
    ):
        return await self.update_by_pk(
            schema=route_in,
            pk_values=pk_values,
        )

    async def delete_route(
            self,
            pk_values,
    ):
        return await self.delete_by_pk(
            pk_values=pk_values,
        )
