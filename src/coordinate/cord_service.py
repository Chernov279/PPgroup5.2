from typing import Annotated, List

from fastapi import Depends

from .cord_dependencies import get_coordinate_uow
from .cord_schemas import CoordinateCreateIn
from .cord_uow import CoordinateUnitOfWork
from .cord_utils import create_cords_create_internal

from ..config.token_config import oauth2_scheme
from ..exceptions.base_exceptions import NoContentResponse
from ..exceptions.coordinate_exceptions import (
    CordsNotFoundException,
    CordPermissionException,
    CordsDeletedException,
    CordFailedDeleteException
)
from ..exceptions.route_exceptions import RouteNotFoundException
from ..models.models import Coordinate, Route
from ..token.token_utils import get_sub_from_token
from ..utils.database_utils import valid_limit, valid_offset


class CoordinateService:
    @staticmethod
    async def get_all_cords_service(
            cord_uow: CoordinateUnitOfWork = Depends(get_coordinate_uow),
            limit: int = 30,
            offset: int = 0,
    ):
        valid_limit(limit),
        valid_offset(offset)

        async with cord_uow as uow:
            coordinates = await uow.get_all_cords_uow(
                selected_columns=Coordinate.get_columns_by_names("latitude", "longitude", "order"),
                limit=limit,
                offset=offset,
            )
        if not coordinates:
            raise CordsNotFoundException()
        return coordinates

    @staticmethod
    async def get_cords_by_route_service(
            route_id: int,
            limit: int = 30,
            offset: int = 0,
            cord_uow: CoordinateUnitOfWork = Depends(get_coordinate_uow)
    ):
        valid_limit(limit),
        valid_offset(offset)

        async with cord_uow as uow:
            coordinates = await uow.get_cords_by_route_uow(
                selected_columns=Coordinate.get_columns_by_names("latitude", "longitude", "order"),
                route_id=route_id)
        if not coordinates:
            raise CordsNotFoundException()
        return coordinates

    @staticmethod
    async def add_cords_by_route_service(
            route_id: int,
            coordinates_in: List[CoordinateCreateIn],
            token: Annotated[str, Depends(oauth2_scheme)],
            cord_uow: CoordinateUnitOfWork = Depends(get_coordinate_uow)
    ):
        user_id = get_sub_from_token(token)
        async with cord_uow as uow:
            user_id_route = await uow.get_user_by_route(
                route_id=route_id,
                selected_columns=[Route.user_id],
            )
            if not user_id_route:
                raise RouteNotFoundException()
            if user_id_route != user_id:
                raise CordPermissionException(action="add coordinates")
            cur_order = await uow.get_current_order(
                route_id=route_id,
            )
            if cur_order is None:
                cur_order = -1
            coordinates_internal = create_cords_create_internal(
                schemas=coordinates_in,
                route_id=route_id,
                user_id=user_id,
                order=cur_order + 1,
            )
            await uow.add_cords_by_route_uow(
                cords_in=coordinates_internal
            )
        return NoContentResponse(status_code=201, detail={"msg": "Coordinates added successfully"}).get_response()

    @staticmethod
    async def delete_all_cords_by_route_service(
            route_id: int,
            token: Annotated[str, Depends(oauth2_scheme)],
            cord_uow: CoordinateUnitOfWork = Depends(get_coordinate_uow)
    ):
        user_id = get_sub_from_token(token)
        async with cord_uow as uow:
            user_id_route = await uow.get_route_by_id_uow(
                route_id=route_id,
                selected_columns=[Coordinate.user_id,],
            )
            if not user_id_route:
                raise CordsNotFoundException()
            if user_id_route != user_id:
                raise CordPermissionException(action="delete coordinates")

            is_deleted = await uow.delete_all_cords_by_route_uow(route_id=route_id)
            if not is_deleted:
                raise CordFailedDeleteException()

        return CordsDeletedException().get_response()
