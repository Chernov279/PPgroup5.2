from typing import Optional, List

from src.exceptions.route_exceptions import RouteNotFoundException
from src.rating_route.rat_repository import RatingRepository
from src.repositories.sqlalchemy_uow import SqlAlchemyUnitOfWork
from src.route.route_repository import RouteRepository


class RatingUnitOfWork(SqlAlchemyUnitOfWork):
    def __init__(self, db_session):
        super().__init__(db_session)
        self.db_session = db_session
        self.repository = RatingRepository(db_session)

    async def get_all_ratings_uow(
            self,
            selected_columns: Optional[List] = None,
            limit: int = 30,
            offset: int = 0,
    ):
        try:
            ratings = await self.repository.get_all_ratings(
                selected_columns=selected_columns,
                limit=limit,
                offset=offset,
            )
            return ratings
        except Exception as e:
            raise e

    async def get_rating_by_pks_uow(
            self,
            pks,
            selected_columns: Optional[List] = None,
    ):
        try:
            ratings = await self.repository.get_rating_by_pks(
                selected_columns=selected_columns,
                pks=pks,
            )
            return ratings
        except Exception as e:
            raise e

    async def get_all_my_ratings_uow(
            self,
            user_id: int,
            selected_columns: Optional[List] = None,
            limit: int = 30,
            offset: int = 0,
    ):
        try:
            ratings = await self.repository.get_all_my_ratings(
                user_id=user_id,
                selected_columns=selected_columns,
                limit=limit,
                offset=offset,

            )
            return ratings
        except Exception as e:
            raise e

    async def create_rating_uow(
            self,
            rating_in,
            selected_columns
    ):
        try:
            route = await RouteRepository(self.db_session).get_route_by_id(route_id=rating_in.route_id)
            if not route:
                raise RouteNotFoundException()
            rating = await self.repository.create_rating(
                rating_in=rating_in,
                selected_columns=selected_columns
            )
            await self.db_session.commit()
            return rating
        except Exception as e:
            raise e

    async def update_rating_uow(self, rating_in):
        try:
            rating = await self.repository.update_rating(rating_in)
            await self.db_session.commit()
            return rating
        except Exception as e:
            raise e

    async def delete_rating_by_pks(self, pks):
        try:
            deleted = await self.repository.delete_rating(
                user_id=pks.user_id,
                route_id=pks.route_id
            )
            await self.db_session.commit()
            return deleted
        except Exception as e:
            raise e
