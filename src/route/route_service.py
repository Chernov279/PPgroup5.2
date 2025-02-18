from typing import Annotated

from fastapi import Depends

from ..config.token_config import oauth2_scheme
from ..exceptions.base_exceptions import NoContentResponse
from ..exceptions.route_exceptions import (
    RouteNotFoundException,
    RouteFailedCreateException,
    RouteFailedUpdateException,
    RoutePermissionException,
    RouteFailedDeleteException
)
from ..models.models import Route
from ..token.token_utils import get_sub_from_token
from ..utils.database_utils import valid_limit, valid_offset
from ..utils.schema_utils import add_internal_params, delete_none_params

from .route_schemas import (
    RouteOut,
    RouteCreateIn,
    RouteCreateInternal,
    RouteUpdateIn
)
from .route_dependencies import get_route_uow
from .route_uow import RouteUnitOfWork
from .route_utils import create_route_detail_by_model


class RouteService:
    @staticmethod
    async def get_all_routes_service(
            limit: int = 30,
            offset: int = 0,
            route_uow: RouteUnitOfWork = Depends(get_route_uow)
    ):
        valid_limit(limit),
        valid_offset(offset)

        selected_columns = RouteOut.get_selected_columns()
        async with route_uow as uow:
            routes = await uow.get_all_routes_uow(
                limit=limit,
                offset=offset,
                selected_columns=selected_columns
            )
        return routes

    @staticmethod
    async def get_my_routes_service(
            token: Annotated[str, Depends(oauth2_scheme)],
            limit: int = 30,
            offset: int = 0,
            route_uow: RouteUnitOfWork = Depends(get_route_uow)
    ):
        user_id = get_sub_from_token(token)
        valid_limit(limit),
        valid_offset(offset)

        selected_columns = RouteOut.get_selected_columns()
        async with route_uow as uow:
            routes = await uow.get_routes_by_user_id_uow(
                user_id=user_id,
                limit=limit,
                offset=offset,
                selected_columns=selected_columns
            )
        return routes

    @staticmethod
    async def get_route_detail_service(
            route_id: int,
            route_uow: RouteUnitOfWork = Depends(get_route_uow)
    ):
        selected_columns = RouteOut.get_selected_columns()
        async with route_uow as uow:
            route = await uow.get_route_by_id_uow(
                route_id=route_id,
                selected_columns=selected_columns
            )
            if not route:
                raise RouteNotFoundException(route_id)
            route_details = await uow.get_route_detail_params_uow(
                user_id=route.user_id,
                route_id=route_id,
            )
        detail_route = create_route_detail_by_model(route, route_details, raise_exception=False)
        return detail_route

    @staticmethod
    async def get_route_by_id_service(
            route_id: int,
            route_uow: RouteUnitOfWork = Depends(get_route_uow)
    ):
        selected_columns = RouteOut.get_selected_columns()
        async with route_uow as uow:
            route = await uow.get_route_by_id_uow(
                route_id=route_id,
                selected_columns=selected_columns
            )
        if not route:
            raise RouteNotFoundException(route_id)
        return route

    @staticmethod
    async def create_route_service(
            token: Annotated[str, Depends(oauth2_scheme)],
            route_in: RouteCreateIn,
            route_uow: RouteUnitOfWork = Depends(get_route_uow)
    ):
        user_id = get_sub_from_token(token)
        route_internal = add_internal_params(route_in, RouteCreateInternal, user_id=user_id)

        async with route_uow as uow:
            route = await uow.create_route_uow(route_in=route_internal, flush=True)
        if not route:
            raise RouteFailedCreateException()
        return route

    @staticmethod
    async def update_route_service(
            route_in: RouteUpdateIn,
            token: Annotated[str, Depends(oauth2_scheme)],
            route_uow: RouteUnitOfWork = Depends(get_route_uow)
    ):
        user_id = get_sub_from_token(token)
        delete_none_params(route_in)
        async with route_uow as uow:
            user_id_route = await uow.get_route_by_id_uow(route_id=route_in.id, selected_columns=[Route.user_id])
            if user_id_route != user_id:
                raise RoutePermissionException(action="update")
            route = await uow.update_route_uow(route_in)
            if not route:
                raise RouteFailedUpdateException()
            return route

    @staticmethod
    async def delete_route_service(
            route_id: int,
            token: Annotated[str, Depends(oauth2_scheme)],
            route_uow: RouteUnitOfWork = Depends(get_route_uow)
    ):
        user_id = get_sub_from_token(token)

        async with route_uow as uow:
            user_id_route = await uow.get_route_by_id_uow(route_id=route_id, selected_columns=[Route.user_id], scalar=True)
            if not user_id_route:
                raise RouteNotFoundException()
            if user_id_route != user_id:
                raise RoutePermissionException(action="delete")
            is_deleted = await uow.delete_route_uow(route_id)
            if not is_deleted:
                raise RouteFailedDeleteException()

        return NoContentResponse(status_code=204, detail={"msg": "Route was successfully deleted"}).get_response()
