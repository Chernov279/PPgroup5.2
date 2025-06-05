from typing import Annotated

from fastapi import Depends

from src.config.token_config import oauth2_scheme
from src.exceptions.rating_exceptions import RatingNotFoundException, RatingAlreadyExistsException, \
    RatingFailedActionException
from src.rating_route.rat_dependencies import get_rating_uow
from src.rating_route.rat_schemas import RatingPKs, RatingShortOut, RatingCreateIn, RatingCreateInInternal, \
    RatingUpdateIn, RatingUpdateInternal
from src.rating_route.rat_uow import RatingUnitOfWork
from src.redis.avg_rat_cache import AvgRatingCache
from src.redis.redis_dependencies import get_avg_rat_cache
from src.schemas.database_params_schemas import MultiGetParams
from src.token.token_utils import get_sub_from_token
from src.utils.schema_utils import add_internal_params


class RatingService:
    @staticmethod
    async def get_all_ratings(
            rating_uow: RatingUnitOfWork = Depends(get_rating_uow),
            multi_get_params: MultiGetParams = Depends(),
    ):

        ratings = await rating_uow.get_all_ratings_uow(
            selected_columns=RatingShortOut.get_selected_columns(),
            **multi_get_params.model_dump(),
        )
        if not ratings:
            raise RatingNotFoundException()
        return ratings

    @staticmethod
    async def get_rating_by_pks(
            primary_keys: Annotated[RatingPKs, Depends()],
            rating_uow: RatingUnitOfWork = Depends(get_rating_uow),
):

        rating = await rating_uow.get_rating_by_pks_uow(
            selected_columns=RatingShortOut.get_selected_columns(),
            pks=primary_keys
        )
        if not rating:
            raise RatingNotFoundException()
        return rating

    @staticmethod
    async def get_all_my_ratings(
            token: Annotated[str, Depends(oauth2_scheme)],
            rating_uow: RatingUnitOfWork = Depends(get_rating_uow),
            multi_get_params: MultiGetParams = Depends(),
    ):
        user_id = get_sub_from_token(token)

        async with rating_uow as uow:
            ratings = await uow.get_all_my_ratings_uow(
                selected_columns=RatingShortOut.get_selected_columns(),
                user_id=user_id,
                **multi_get_params.model_dump(),
            )
        if not ratings:
            raise RatingNotFoundException()
        return ratings

    @staticmethod
    async def get_my_rating_by_route(
            token: Annotated[str, Depends(oauth2_scheme)],
            route_id: int,
            rating_uow: RatingUnitOfWork = Depends(get_rating_uow),
    ):
        user_id = get_sub_from_token(token)

        primary_keys = add_internal_params(None, RatingPKs, user_id=user_id, route_id=route_id)

        rating = await rating_uow.get_rating_by_pks_uow(
            selected_columns=RatingShortOut.get_selected_columns(),
            pks=primary_keys
        )
        if not rating:
            raise RatingNotFoundException()
        return rating

    @staticmethod
    async def create_rating(
            rating_in: RatingCreateIn,
            token: Annotated[str, Depends(oauth2_scheme)],
            rating_uow: RatingUnitOfWork = Depends(get_rating_uow),
            avg_rat_cache: AvgRatingCache = Depends(get_avg_rat_cache),
    ):
        user_id = get_sub_from_token(token)
        pks = add_internal_params(None, RatingPKs, user_id=user_id, route_id=rating_in.route_id)

        old_rating = await rating_uow.get_rating_by_pks_uow(
            selected_columns=RatingShortOut.get_selected_columns(),
            pks=pks
        )
        if old_rating:
            raise RatingAlreadyExistsException()
        rating_internal = add_internal_params(rating_in, RatingCreateInInternal, user_id=user_id)

        new_rating = await rating_uow.create_rating_uow(
            selected_columns=RatingShortOut.get_selected_columns(),
            rating_in=rating_internal
        )

        if not new_rating:
            raise RatingNotFoundException()

        await avg_rat_cache.invalidate(route_id=rating_in.route_id)

        return new_rating

    @staticmethod
    async def update_rating_by_route(
            rating_in: RatingUpdateIn,
            token: Annotated[str, Depends(oauth2_scheme)],
            rating_uow: RatingUnitOfWork = Depends(get_rating_uow),
            avg_rat_cache: AvgRatingCache = Depends(get_avg_rat_cache),
    ):

        user_id = get_sub_from_token(token)
        rating_internal = add_internal_params(rating_in, RatingUpdateInternal, user_id=user_id)

        updated_rating = await rating_uow.update_rating_uow(
            # selected_columns=RatingShortOut.get_selected_columns(),
            rating_in=rating_internal
        )
        await avg_rat_cache.invalidate(route_id=rating_in.route_id)

        return updated_rating

    @staticmethod
    async def delete_rating_by_route(
            route_id: int,
            token: Annotated[str, Depends(oauth2_scheme)],
            rating_uow: RatingUnitOfWork = Depends(get_rating_uow),
            avg_rat_cache: AvgRatingCache = Depends(get_avg_rat_cache)
    ):
        user_id = get_sub_from_token(token)
        pks = add_internal_params(None, RatingPKs, user_id=user_id, route_id=route_id)

        is_deleted = await rating_uow.delete_rating_by_pks(
            pks=pks
        )
        if not is_deleted:
            raise RatingFailedActionException("delete rating")

        await avg_rat_cache.invalidate(route_id=route_id)

        return {"message": "successfully deleted"}

    @staticmethod
    async def get_avg_rating_by_route(
            route_id: int,
            rating_uow: RatingUnitOfWork = Depends(get_rating_uow),
            avg_rat_cache: AvgRatingCache = Depends(get_avg_rat_cache)
    ):
        avg_rating = await avg_rat_cache.get_rating(route_id)
        if avg_rating is None:
            avg_rating = await rating_uow.get_avg_rating_by_route_uow(route_id)
        if avg_rating is not None:
            avg_rating = round(float(avg_rating), 2)
            await avg_rat_cache.set_rating(route_id, avg_rating)
            return {"value": avg_rating}
        raise RatingFailedActionException("get average rating", 404)
