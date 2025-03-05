from typing import Optional, List

from src.coordinate.cord_repository import CoordinateRepository
from src.repositories.sqlalchemy_uow import SqlAlchemyUnitOfWork


class CoordinateUnitOfWork(SqlAlchemyUnitOfWork):
    def __init__(self, db_session):
        super().__init__(db_session)
        self.db_session = db_session
        self.repository = CoordinateRepository(db_session)

    async def get_all_cords_uow(
            self,
            selected_columns: Optional[List] = None,
            limit: int = 30,
            offset: int = 0,
    ):
        try:
            coordinates = await self.repository.get_all_cords(
                selected_columns=selected_columns,
                limit=limit,
                offset=offset,
            )
            return coordinates
        except Exception as e:
            raise e

    async def get_cords_by_route_uow(
            self,
            route_id: int,
            limit: int = 30,
            offset: int = 0,
            selected_columns: Optional[List] = None,
    ):
        try:
            coordinates = await self.repository.get_cords_by_route(
                route_id=route_id,
                selected_columns=selected_columns,
                limit=limit,
                offset=offset,
            )
            return coordinates
        except Exception as e:
            raise e

    async def get_user_by_route(
            self,
            route_id,
            selected_columns,
    ):
        from src.route.route_repository import RouteRepository
        route_repo = RouteRepository(self.db_session)
        try:
            user_id = await route_repo.get_route_by_id(
                route_id=route_id,
                selected_columns=selected_columns,
                scalar=True
            )
            return user_id
        except Exception as e:
            raise e

    async def get_current_order(
        self,
        route_id,
    ):
        try:
            cur_order = await self.repository.get_latest_order(
                route_id=route_id,
            )
            return cur_order
        except Exception as e:
            raise e

    async def add_cord_by_route_uow(
            self,
            cord_in,
    ):
        try:
            coordinates = await self.repository.add_cord(
                cord_in=cord_in
            )
            await self.db_session.commit()
            return coordinates
        except Exception as e:
            raise e

    async def add_cords_by_route_uow(
            self,
            cords_in,
    ):
        try:
            coordinates = await self.repository.add_cords(
                cords_in=cords_in
            )
            await self.db_session.commit()
            return coordinates
        except Exception as e:
            raise e

    async def delete_all_cords_by_route_uow(self, route_id: int):
        try:
            deleted = await self.repository.delete_cords_by_route(
                route_id=route_id
            )
            await self.db_session.commit()
            return deleted
        except Exception as e:
            raise e