from typing import Annotated, List

from fastapi import APIRouter, Depends

from .route_dependencies import get_route_service_db
from .route_schemas import RouteOut, RouteCreateIn, RouteUpdateIn, RouteDetailOut
from .route_service import RouteService
from ..config.token_config import oauth2_scheme

route = APIRouter(prefix="/routes", tags=["Route"])


@route.get("/", response_model=List[RouteOut])
def get_all_routes_endpoint(
        service: Annotated[RouteService, Depends(get_route_service_db)]
):
    return service.get_routes_service()


@route.get("/my", response_model=List[RouteOut])
def get_my_routes_endpoint(
        token: Annotated[str, Depends(oauth2_scheme)],
        service: Annotated[RouteService, Depends(get_route_service_db)]
):
    return service.get_my_routes_service(token)


@route.get("/detail", response_model=RouteDetailOut)
def get_route_detail_endpoint(
        route_id: int,
        token: Annotated[str, Depends(oauth2_scheme)],
        service: Annotated[RouteService, Depends(get_route_service_db)]
):
    return service.get_route_detail_service(route_id, token)


@route.get("/{route_id}", response_model=RouteOut)
def get_route_by_id_endpoint(
        route_id: int,
        service: Annotated[RouteService, Depends(get_route_service_db)]
):
    return service.get_route_by_id_service(route_id)


@route.post("/", response_model=RouteOut)
def create_route_endpoint(
        route_in: RouteCreateIn,
        token: Annotated[str, Depends(oauth2_scheme)],
        service: Annotated[RouteService, Depends(get_route_service_db)]
):
    return service.create_route_service(route_in, token)


@route.put("/{route_in.id}")
def update_route_endpoint(
        route_in: RouteUpdateIn,
        token: Annotated[str, Depends(oauth2_scheme)],
        service: Annotated[RouteService, Depends(get_route_service_db)]
):
    return service.update_route_service(route_in, token)


@route.delete("/{route_id}")
def delete_route_endpoint(
        route_id: int,
        token: Annotated[str, Depends(oauth2_scheme)],
        service: Annotated[RouteService, Depends(get_route_service_db)]
):
    return service.delete_route_service(route_id, token)
