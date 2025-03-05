from typing import Annotated, List

from fastapi import APIRouter, Depends

from .cord_schemas import CoordinateOut
from .cord_service import CoordinateService

coordinate = APIRouter(prefix="/cord", tags=["Coordinate of route"])


@coordinate.get("/", response_model=List[CoordinateOut])
async def get_all_coordinates_endpoint(
        coordinates_out: Annotated[List[CoordinateOut], Depends(CoordinateService.get_all_cords_service)]
):
    return coordinates_out


@coordinate.get("/{route_id}", response_model=List[CoordinateOut])
async def get_route_coordinates_endpoint(
        coordinates_out: Annotated[List[CoordinateOut], Depends(CoordinateService.get_cords_by_route_service)]
):
    return coordinates_out


@coordinate.post("/{route_id}")
async def add_route_coordinates_endpoint(
        cord_out: Annotated[None, Depends(CoordinateService.add_cords_by_route_service)]
):
    return cord_out


@coordinate.delete("/{route_id}")
async def delete_all_route_coordinates_endpoint(
        cord_out: Annotated[None, Depends(CoordinateService.delete_all_cords_by_route_service)]
):
    return cord_out
