from typing import Annotated

from fastapi import Depends

from src.config.token_config import oauth2_scheme
from src.exceptions.rating_exceptions import RatingNotFoundException, RatingAlreadyExistsException, \
    RatingFailedActionException
from src.rating_route.rat_dependencies import get_rating_uow
from src.rating_route.rat_schemas import RatingPKs, RatingShortOut, RatingCreateIn, RatingCreateInInternal, \
    RatingUpdateIn, RatingUpdateInternal
from src.rating_route.rat_uow import RatingUnitOfWork
from src.token.token_utils import get_sub_from_token
from src.utils.database_utils import valid_limit, valid_offset
from src.utils.schema_utils import add_internal_params


class RatingService:
    @staticmethod
    async def get_all_ratings(
            rating_uow: RatingUnitOfWork = Depends(get_rating_uow),
            limit: int = 30,
            offset: int = 0,
    ):
        valid_limit(limit)
        valid_offset(offset)

        async with rating_uow as uow:
            ratings = await uow.get_all_ratings_uow(
                selected_columns=RatingShortOut.get_selected_columns(),
                limit=limit,
                offset=offset,
            )
        if not ratings:
            raise RatingNotFoundException()
        return ratings

    @staticmethod
    async def get_rating_by_pks(
            primary_keys: Annotated[RatingPKs, Depends()],
            rating_uow: RatingUnitOfWork = Depends(get_rating_uow),
):
        async with rating_uow as uow:
            rating = await uow.get_rating_by_pks_uow(
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
            limit: int = 30,
            offset: int = 0,
    ):
        user_id = get_sub_from_token(token)

        async with rating_uow as uow:
            ratings = await uow.get_all_my_ratings_uow(
                selected_columns=RatingShortOut.get_selected_columns(),
                user_id=user_id,
                limit=limit,
                offset=offset,
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
        async with rating_uow as uow:
            rating = await uow.get_rating_by_pks_uow(
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
    ):
        user_id = get_sub_from_token(token)
        pks = add_internal_params(None, RatingPKs, user_id=user_id, route_id=rating_in.route_id)

        async with rating_uow as uow:
            old_rating = await uow.get_rating_by_pks_uow(
                selected_columns=RatingShortOut.get_selected_columns(),
                pks=pks
            )
            if old_rating:
                raise RatingAlreadyExistsException()
            rating_internal = add_internal_params(rating_in, RatingCreateInInternal, user_id=user_id)

            new_rating = await uow.create_rating_uow(
                selected_columns=RatingShortOut.get_selected_columns(),
                rating_in=rating_internal
            )

        if not new_rating:
            raise RatingNotFoundException()
        return new_rating

    @staticmethod
    async def update_rating_by_route(
            rating_in: RatingUpdateIn,
            token: Annotated[str, Depends(oauth2_scheme)],
            rating_uow: RatingUnitOfWork = Depends(get_rating_uow),
    ):

        user_id = get_sub_from_token(token)
        rating_internal = add_internal_params(rating_in, RatingUpdateInternal, user_id=user_id)

        async with rating_uow as uow:
            updated_rating = await uow.update_rating_uow(
                # selected_columns=RatingShortOut.get_selected_columns(),
                rating_in=rating_internal
            )

        return updated_rating

    @staticmethod
    async def delete_rating_by_route(
            route_id: int,
            token: Annotated[str, Depends(oauth2_scheme)],
            rating_uow: RatingUnitOfWork = Depends(get_rating_uow),
    ):
        user_id = get_sub_from_token(token)
        pks = add_internal_params(None, RatingPKs, user_id=user_id, route_id=route_id)

        async with rating_uow as uow:
            is_deleted = await uow.delete_rating_by_pks(
                pks=pks
            )
        if not is_deleted:
            raise RatingFailedActionException("delete rating")
        return {"message": "successfully deleted"}

