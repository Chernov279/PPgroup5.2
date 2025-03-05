from typing import Annotated, List

from fastapi import APIRouter, Depends
from .rat_schemas import RatingOut
from .rat_service import RatingService
rating = APIRouter(prefix="/rating", tags=["Rating of routes"])


@rating.get("/")
def get_rating_by_id_endpoint(
        rating_out: Annotated[RatingOut, Depends(RatingService().get_rating_by_fk)]
):
    return rating_out


@rating.get("/all", response_model=List[RatingOut])
def get_all_ratings_endpoint(
        rating_out: Annotated[RatingOut, Depends(RatingService().get_all_ratings)]
):
    return rating_out


@rating.get("/my", response_model=List[RatingOut])
def get_all_ratings_endpoint(
        rating_out: Annotated[RatingOut, Depends(RatingService().get_all_my_ratings)]
):
    return rating_out


@rating.get("/{route_id}", response_model=RatingOut)
def get_my_rating_by_route_id(
        rating_out: Annotated[RatingOut, Depends(RatingService().get_my_rating_by_route_id)]
):
    return rating_out


@rating.post("/", response_model=RatingOut)
def create_rating_endpoint(
        rating_out: Annotated[RatingOut, Depends(RatingService().create_rating)]
):
    return rating_out


@rating.put("/", response_model=RatingOut)
def update_rating_by_id_endpoint(
        rating_out: Annotated[RatingOut, Depends(RatingService().update_rating_by_fk)]
):
    return rating_out

@rating.delete("/")
def delete_rating_by_id_endpoint(
        rating_out: Annotated[RatingOut, Depends(RatingService().delete_rating_by_fk)]
):
    return rating_out

