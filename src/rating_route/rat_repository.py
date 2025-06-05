from src.models.models import Rating
from src.repositories.sqlalchemy_repository import SQLAlchemyRepository


class RatingRepository(SQLAlchemyRepository):
    def __init__(self, db_session):
        super().__init__(db_session, Rating)

    async def get_rating_by_pks(self, selected_columns, pks):
        return await self.get_single(
            selected_columns=selected_columns,
            user_id=pks.user_id,
            route_id=pks.route_id,
        )

    async def get_all_ratings(self, selected_columns, limit, offset):
        return await self.get_multi(
            selected_columns=selected_columns,
            limit=limit,
            offset=offset,
            order="created_at"
        )

    async def get_all_my_ratings(self, selected_columns, limit, offset, user_id):
        return await self.get_multi_with_filters(
            selected_columns=selected_columns,
            limit=limit,
            offset=offset,
            order="created_at",
            user_id=user_id,
        )

    async def get_count_ratings(self):
        return await self.get_count_by_filters(

        )

    async def get_avg_rating_by_route(
            self,
            route_id
    ):
        return await self.get_avg_by_filters(
            column_name="value",
            route_id=route_id
        )

    async def create_rating(self, rating_in, selected_columns):
        return await self.create(
            schema=rating_in,
            selected_columns=selected_columns,
            flush=True
        )

    async def update_rating(self, rating_in):
        return await self.update(
            schema=rating_in,
            user_id=rating_in.user_id,
            route_id=rating_in.route_id
        )

    async def delete_rating(self, user_id, route_id):
        return await self.delete(
            user_id=user_id,
            route_id=route_id
        )
