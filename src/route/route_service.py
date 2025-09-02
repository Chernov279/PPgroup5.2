import logging

from fastapi import Depends

from ..exceptions.base_exceptions import NoContentResponse
from ..exceptions.route_exceptions import (
    RouteNotFoundException,
    RouteFailedCreateException,
    RouteFailedUpdateException,
    RoutePermissionException,
    RouteFailedDeleteException
)
from ..models.models import Route
from ..schemas.database_params_schemas import MultiGetParams
from ..token_app.token_utils import get_sub_from_token
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

logger = logging.getLogger(__name__)


class RouteService:
    def __init__(
            self,
            route_uow: RouteUnitOfWork = Depends(get_route_uow)
    ):
        self._route_uow = route_uow

    async def get_all_routes_service(
            self,
            multi_get_params: MultiGetParams
    ):
        logger.info("Incoming request to get_all_routes")

        selected_columns = RouteOut.get_selected_columns()

        routes = await self._route_uow.get_all_routes_uow(
            **multi_get_params.model_dump(),
            selected_columns=selected_columns
        )
        return routes

    async def get_my_routes_service(
            self,
            token: str,
            multi_get_params: MultiGetParams,
    ):
        user_id = get_sub_from_token(token)
        logger.info("Incoming request to get_my_routes")

        selected_columns = RouteOut.get_selected_columns()

        routes = await self._route_uow.get_routes_by_user_id_uow(
            user_id=user_id,
            **multi_get_params.model_dump(),
            selected_columns=selected_columns
        )
        return routes

    async def get_route_detail_service(
            self,
            route_id: int,
    ):
        logger.info("Incoming request to get_route_detail route_id=s%", route_id)

        selected_columns = RouteOut.get_selected_columns()

        route = await self._route_uow.get_route_by_id_uow(
            route_id=route_id,
            selected_columns=selected_columns
        )
        if not route:
            logger.info("Request to get_route_detail not found route_id=s%", route_id)
            raise RouteNotFoundException(route_id)
        route_details = await self._route_uow.get_route_detail_params_uow(
            user_id=route.user_id,
            route_id=route_id,
        )

        detail_route = create_route_detail_by_model(route, route_details, raise_exception=False)
        return detail_route

    async def get_route_by_id_service(
            self,
            route_id: int,
    ):
        logger.info("Incoming request to get_route_by_id route_id=s%", route_id)

        selected_columns = RouteOut.get_selected_columns()

        route = await self._route_uow.get_route_by_id_uow(
            route_id=route_id,
            selected_columns=selected_columns
        )
        if not route:
            raise RouteNotFoundException(route_id)
        return route

    async def create_route_service(
            self,
            token: str,
            route_in: RouteCreateIn,
    ):
        logger.info("Incoming request to create_route")

        user_id = get_sub_from_token(token)
        route_internal = add_internal_params(route_in, RouteCreateInternal, user_id=user_id)

        route = await self._route_uow.create_route_uow(route_in=route_internal, flush=True)

        if not route:
            logger.info("Request to create_route failed")
            raise RouteFailedCreateException()
        return route

    async def update_route_service(
            self,
            token: str,
            route_id: int,
            route_in: RouteUpdateIn,
    ):
        logger.info("Incoming request to update_route route_id=s%", route_id)
        user_id = get_sub_from_token(token)
        delete_none_params(route_in)

        user_id_route = await self._route_uow.get_route_by_id_uow(route_id=route_id, selected_columns=[Route.user_id])
        if user_id_route != user_id:
            logger.info(
                "Request to update_route: user have no permission to update route_id=s% token_user_id=s%",
                route_id, user_id
            )
            raise RoutePermissionException(action="update")
        route = await self._route_uow.update_route_uow(route_in, route_id)
        if not route:
            logger.info("Request to update_route failed")
            raise RouteFailedUpdateException()
        return route

    async def delete_route_service(
            self,
            token: str,
            route_id: int,

    ):
        logger.info("Incoming request to delete_route route_id=s%", route_id)
        user_id = get_sub_from_token(token)

        user_id_route = await self._route_uow.get_route_by_id_uow(
            route_id=route_id,
            selected_columns=[Route.user_id],
            scalar=True
        )
        if not user_id_route:
            logger.info("Request to delete_route not found route_id=s%", route_id)
            raise RouteNotFoundException()
        if user_id_route != user_id:
            logger.info(
                "Request to delete_route_service: user have no permission to felete route_id=s% token_user_id=s%",
                route_id, user_id
            )
            raise RoutePermissionException(action="delete")
        is_deleted = await self._route_uow.delete_route_uow(route_id)
        if not is_deleted:
            logger.info("Request to delete_route failed")
            raise RouteFailedDeleteException()

        return NoContentResponse(status_code=204, detail={"msg": "Route was successfully deleted"}).get_response()
