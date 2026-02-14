

from src.db.models.models import Rating
from src.db.repositories.sqlalchemy_repository import SQLAlchemyRepository


class RatingRepository(SQLAlchemyRepository):
    def __init__(self, db_session):
        super().__init__(db_session, Rating)

    async def get_rating_by_pks(self, selected_columns, pks):
        pass

    async def get_all_ratings(self, selected_columns, limit, offset):
        pass

    async def get_all_my_ratings(self, selected_columns, limit, offset, user_id):
        pass

    async def get_count_ratings(self):
        pass

    async def get_avg_rating_by_route(
            self,
            route_id
    ):
        pass

    async def create_rating(self, rating_in, selected_columns):
        pass

    async def update_rating(self, rating_in):
        pass

    async def delete_rating(self, user_id, route_id):
        pass
