from typing import Annotated, List

from fastapi import APIRouter, Depends
from starlette import status

from .route_schemas import RouteOut, RouteDetailOut, RouteCreateIn, RouteUpdateIn
from .route_service import RouteService
from ..config.token_config import oauth2_scheme
from ..schemas.database_params_schemas import MultiGetParams

route = APIRouter(prefix="/routes", tags=["Route"])


@route.get(
   "/",
   response_model=List[RouteOut],
   summary="List all routes",
   description="Return paginated list of routes. Supports query params for pagination.",
   responses={
       200: {"description": "List of routes"},
       204: {"description": "No routes found"},
   },
)
async def get_all_routes_endpoint(
        multi_get_params: MultiGetParams = Depends(),
        route_service: RouteService = Depends()
):
    return await route_service.get_all_routes_service(multi_get_params)


@route.get(
    "/my",
    response_model=List[RouteOut],
    summary="List my routes",
    description="Return routes for the authenticated user, else authentication exception",
    responses={
        200: {"description": "List of user's routes"},
        401: {"description": "Unauthorized"}
    },
)
async def get_my_routes_endpoint(
        token: Annotated[str, Depends(oauth2_scheme)],
        multi_get_params: MultiGetParams = Depends(),
        route_service: RouteService = Depends()
):
    return await route_service.get_my_routes_service(token, multi_get_params)


@route.get(
    "/{route_id}/detail",
    response_model=RouteDetailOut,
    summary="Route detail",
    description="Get route detail including coordinates and extra meta.",
    responses={
        200: {"description": "Detailed route"},
        404: {"description": "Route not found"},
    },
)
async def get_route_detail_endpoint(
        route_id: int,
        route_service: RouteService = Depends()
):
    return await route_service.get_route_detail_service(route_id)


@route.get(
    "/{route_id}",
    response_model=RouteOut,
    summary="Get route by id",
    description="Get short info for a single route.",
    responses={
        200: {"description": "Route found"},
        404: {"description": "Route not found"}
    },
)
async def get_route_by_id_endpoint(
        route_id: int,
        route_service: RouteService = Depends()
):
    return await route_service.get_route_by_id_service(route_id)


@route.post(
    "/",
    response_model=RouteOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create route",
    description="Create a new route for the authenticated user.",
    responses={
        201: {"description": "Route created"},
        400: {"description": "Bad request"},
        401: {"description": "Unauthorized"},
    },
)
async def create_route_endpoint(
        token: Annotated[str, Depends(oauth2_scheme)],
        route_in: RouteCreateIn,
        route_service: RouteService = Depends()
):
    return await route_service.create_route_service(token, route_in)


@route.put(
    "/{route_id}",
    status_code=status.HTTP_200_OK,
    summary="Update route",
    description="Update route data. Only owner can update the route",
    responses={
        200: {"description": "Route updated"},
        403: {"description": "Forbidden"}
    },
)
async def update_route_endpoint(
        token: Annotated[str, Depends(oauth2_scheme)],
        route_id: int,
        route_in: RouteUpdateIn,
        route_service: RouteService = Depends(),
):
    return await route_service.update_route_service(token, route_id, route_in)


@route.delete(
    "/{route_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete route",
    description="Delete a route. Only owner can delete it.",
    responses={
        204: {"description": "Deleted"},
        403: {"description": "Forbidden"},
        404: {"description": "Route not found"}
    },
)
async def delete_route_endpoint(
        token: Annotated[str, Depends(oauth2_scheme)],
        route_id: int,
        route_service: RouteService = Depends()
):
    return await route_service.delete_route_service(token, route_id)
