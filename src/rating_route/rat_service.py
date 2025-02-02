from typing import Annotated, List

from fastapi import Depends

from src.config.database.db_helper import get_db
from src.config.token_config import oauth2_scheme
from src.exceptions.rating_exceptions import RatingNotFoundException, RatingFailedActionException, \
    RatingAlreadyExistsException
from src.exceptions.route_exceptions import RouteNotFoundException
from src.exceptions.token_exceptions import InvalidTokenUserException
from src.models.models import Rating
from src.rating_route.rat_repository import RatingRepository
from src.rating_route.rat_schemas import RatingCreateIn, RatingUpdateIn, RatingUpdateInInternal, \
    RatingCreateInInternal
from src.unit_of_work.route_uow import RouteUOW
from src.unit_of_work.token_uow import TokenUOW


class RatingService:
    def get_all_ratings(
            self,
            db_session=Depends(get_db)
    ) -> List[Rating]:
        ratings = RatingRepository(db_session).get_rats_all()
        return ratings

    def get_rating_by_fk(
            self,
            user_id: int,
            route_id: int,
            db_session=Depends(get_db)
) -> Rating:
        rating = RatingRepository(db_session).get_rat_by_ids(user_id=user_id, route_id=route_id)
        if not rating:
            raise RatingNotFoundException()
        return rating

    def get_all_my_ratings(
            self,
            token: Annotated[str, Depends(oauth2_scheme)],
            db_session=Depends(get_db),
    ):
        user_id = TokenUOW(db_session).user_exists_by_token_uow(token)
        if not user_id:
            raise InvalidTokenUserException(user_id)

        ratings = RatingRepository(db_session).get_rats_by_user_id(user_id=user_id)
        return ratings

    def get_my_rating_by_route_id(
            self,
            token: Annotated[str, Depends(oauth2_scheme)],
            route_id: int,
            db_session=Depends(get_db)
    ) -> Rating:
        user_id = TokenUOW(db_session).user_exists_by_token_uow(token)
        if not user_id:
            raise InvalidTokenUserException(user_id)

        rating = RatingRepository(db_session).get_rat_by_ids(user_id=user_id, route_id=route_id)
        if not rating:
            raise RatingNotFoundException()
        return rating

    def create_rating(
            self,
            rating_in: RatingCreateIn,
            token: Annotated[str, Depends(oauth2_scheme)],
            db_session=Depends(get_db)
    ) -> Rating:
        repo = RatingRepository(db_session)

        user_id = TokenUOW(db_session).user_exists_by_token_uow(token)
        if not user_id:
            raise InvalidTokenUserException(user_id)

        old_rating = repo.get_rat_by_ids(user_id, rating_in.route_id)
        if old_rating:
            raise RatingAlreadyExistsException()

        if not RouteUOW(db_session).is_route_exists_uow(route_id=rating_in.route_id):
            raise RouteNotFoundException(rating_in.route_id)

        internal_rating_in = RatingCreateInInternal(**rating_in.dict(), user_id=user_id)

        rating = repo.create_rat(internal_rating_in)
        if not rating:
            raise RatingFailedActionException("create rating")
        return rating

    def update_rating_by_fk(
            self,
            rating_in: RatingUpdateIn,
            token: Annotated[str, Depends(oauth2_scheme)],
            db_session=Depends(get_db)
    ) -> Rating:

        user_id = TokenUOW(db_session).user_exists_by_token_uow(token)
        if not user_id:
            raise InvalidTokenUserException(user_id)

        route_id = rating_in.route_id

        repo = RatingRepository(db_session)
        old_rating = repo.get_rat_by_ids(user_id, route_id)
        if not old_rating:
            raise RatingNotFoundException(route_id=route_id, user_id=user_id)

        internal_rating_in = RatingUpdateInInternal(**rating_in.dict(), user_id=user_id)
        rating = repo.update_rat(internal_rating_in)
        if not rating:
            raise RatingFailedActionException("update rating")

        return rating

    def delete_rating_by_fk(
            self,
            route_id: int,
            token: Annotated[str, Depends(oauth2_scheme)],
            db_session=Depends(get_db)
    ) -> dict:
        user_id = TokenUOW(db_session).user_exists_by_token_uow(token)
        if not user_id:
            raise InvalidTokenUserException(user_id)

        repo = RatingRepository(db_session)

        rating = repo.delete_rat(user_id, route_id)
        if not rating:
            raise RatingFailedActionException("delete rating")
        return {"message": "successfully deleted"}

