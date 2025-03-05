from typing import Annotated, List

from fastapi import APIRouter, Depends

from .route_schemas import RouteOut, RouteDetailOut
from .route_service import RouteService

route = APIRouter(prefix="/routes", tags=["Route"])


@route.get("/", response_model=List[RouteOut])
async def get_all_routes_endpoint(
        routes_out: Annotated[List[RouteOut], Depends(RouteService.get_all_routes_service)]
):
    return routes_out


@route.get("/my", response_model=List[RouteOut])
async def get_my_routes_endpoint(
        routes_out: Annotated[List[RouteOut], Depends(RouteService.get_my_routes_service)]
):
    return routes_out


@route.get("/detail", response_model=RouteDetailOut)
async def get_route_detail_endpoint(
        route_out: Annotated[RouteDetailOut, Depends(RouteService.get_route_detail_service)]
):
    return route_out


@route.get("/{route_id}", response_model=RouteOut)
async def get_route_by_id_endpoint(
        route_out: Annotated[RouteOut, Depends(RouteService.get_route_by_id_service)]
):
    return route_out


@route.post("/", response_model=RouteOut)
async def create_route_endpoint(
        route_out: Annotated[RouteOut, Depends(RouteService.create_route_service)]
):
    return route_out


@route.put("/")
async def update_route_endpoint(
        route_out: Annotated[RouteOut, Depends(RouteService.update_route_service)]
):
    return route_out


@route.delete("/{route_id}")
async def delete_route_endpoint(
        route_out: Annotated[None, Depends(RouteService.delete_route_service)]
):
    return route_out
