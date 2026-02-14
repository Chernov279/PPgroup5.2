from typing import Optional, List

from src.db.models.models import User
from src.db.repositories.routes import RouteRepository
from src.db.repositories.sqlalchemy_uow import SqlAlchemyUnitOfWork
from src.db.repositories.users import UserRepository



class RouteUnitOfWork(SqlAlchemyUnitOfWork):
    def __init__(self, db_session):
        super().__init__(db_session)
        self.db_session = db_session
        self.repository = RouteRepository(db_session)

    async def get_route_by_id_uow(
            self,
            route_id: int,
            selected_columns: Optional[List] = None,
            scalar=False,
    ):
        try:
            route = await self.repository.get_route_by_id(
                route_id=route_id,
                selected_columns=selected_columns,
                scalar=scalar
            )
            return route
        except Exception as e:
            raise e

    async def get_route_detail_params_uow(
            self,
            user_id: int,
            route_id: int,

    ):
        try:
            
            selected_columns = User.get_columns_by_names("name")
            user_name = await UserRepository(db_session=self.db_session).get_user_model_by_id(user_id=user_id)
            # TODO
            # from src.coordinate.cord_repository import CoordinateRepository
            # amount_points = await CoordinateRepository(db_session=self.db_session).get_amount_cords(
            #     route_id=route_id,
            # )
            amount_points = 0
            # TODO
            # from src.rating_route.rat_repository import RatingRepository
            # amount_ratings = await RatingRepository(db_session=self.db_session).get_amount_ratings(
            #     route_id=route_id,
            # )
            amount_ratings = 0
            # TODO
            # avg_rating = await RatingRepository(db_session=self.db_session).get_avg_rating(
            #     route_id=route_id,
            # )
            avg_rating = 0
            return {
                "user_name": user_name,
                "amount_points": amount_points,
                "amount_ratings": amount_ratings,
                "avg_rating": avg_rating,
            }
        except Exception as e:
            raise e

    async def get_user_by_route_uow(
            self,
            route_id: int,
            selected_columns: Optional[List] = None,
            scalar=False,
    ):
        try:
            return await self.repository.get_route_by_id(
                route_id=route_id,
                selected_columns=selected_columns,
                scalar=scalar
            )

        except Exception as e:
            raise e

    async def get_all_routes_uow(
            self,
            limit,
            offset,
            selected_columns: Optional[List] = None
    ):
        try:
            routes = await self.repository.get_all_routes(
                limit=limit,
                offset=offset,
                selected_columns=selected_columns,
            )
            return routes
        except Exception as e:
            raise e

    async def get_routes_by_user_id_uow(
            self,
            user_id,
            limit,
            offset,
            selected_columns: Optional[List] = None
    ):
        try:
            routes = await self.repository.get_routes_by_user_id(
                user_id=user_id,
                limit=limit,
                offset=offset,
                selected_columns=selected_columns,
            )
            return routes
        except Exception as e:
            raise e

    async def create_route_uow(
            self,
            route_in,
            flush
    ):
        try:
            route = await self.repository.create_route(
                route_in=route_in,
                flush=flush
            )
            await self.db_session.commit()
            return route
        except Exception as e:
            raise e

    async def update_route_uow(
            self,
            route_in,
            route_id
    ):
        try:
            route = await self.repository.update_route(
                route_in=route_in,
                pk_values=[route_id,],
            )
            await self.db_session.commit()
            return route
        except Exception as e:
            raise e

    async def delete_route_uow(
            self,
            route_id,
    ):
        try:
            route = await self.repository.delete_route(
                pk_values=[route_id,],
            )
            await self.db_session.commit()
            return route
        except Exception as e:
            raise e
