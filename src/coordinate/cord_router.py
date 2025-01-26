from typing import Annotated

from fastapi import APIRouter, Depends

from .cord_schemas import CordOut
from .cord_service import CoordinateService

coordinate = APIRouter(prefix="/cord", tags=["Coordinate of route"])


@coordinate.get("/")
def get_all_coordinates(
        coordinates_out: Annotated[CordOut, Depends(CoordinateService().get_all_cords)]
):
    return coordinates_out


@coordinate.get("/{route_id}")
def get_route_coordinates(
        coordinates_out: Annotated[CordOut, Depends(CoordinateService().get_cords_by_route)]
):
    return coordinates_out


@coordinate.post("/{route_id}")
def add_route_coordinates(
        coordinates_out: Annotated[None, Depends(CoordinateService().add_cords_by_route)]
):
    return coordinates_out


@coordinate.delete("/{route_id}")
def delete_all_route_coordinates(
        coordinates_out: Annotated[CordOut, Depends(CoordinateService().delete_all_cords_by_route)]
):
    return coordinates_out
