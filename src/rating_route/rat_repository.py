from src.models.models import Rating
from src.repositories.base_repositories import BaseRepository


class RatingRepository(BaseRepository):
    def __init__(self, db_session):
        super().__init__(db_session)

    def get_rat_by_ids(self, user_id, route_id):
        return self.get_single(Rating, user_id=user_id, route_id=route_id)

    def get_rats_by_route_id(self, route_id):
        return self.get_multi_with_filters(
            Rating,
            route_id=route_id
        )

    def get_rats_by_user_id(self, user_id):
        return self.get_multi_with_filters(
            Rating,
            user_id=user_id,
            order="created_time"
        )

    def get_rats_all(self):
        return self.get_multi(
            Rating,
            order="created_time"
        )

    def create_rat(self, rating_in):
        return self.create(
            Rating,
            rating_in
        )

    def update_rat(self, rating_in):
        return self.update_by_filters(
            Rating,
            schema=rating_in,
            user_id=rating_in.user_id,
            route_id=rating_in.route_id
        )

    def delete_rat(self, user_id, route_id):
        return self.delete_by_filters(
            Rating,
            user_id=user_id,
            route_id=route_id
        )
