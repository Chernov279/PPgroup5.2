from typing import Annotated, List

from fastapi import APIRouter, Depends

from .rat_schemas import RatingShortOut, RatingAvgValue
from .rat_service import RatingService

rating = APIRouter(prefix="/rating", tags=["Rating of routes"])


@rating.get("/", response_model=List[RatingShortOut])
async def get_all_ratings_endpoint(
        rating_out: Annotated[RatingShortOut, Depends(RatingService.get_all_ratings)]
):
    return rating_out


@rating.get("/my", response_model=List[RatingShortOut])
async def get_my_ratings_endpoint(
        rating_out: Annotated[RatingShortOut, Depends(RatingService.get_all_my_ratings)]
):
    return rating_out


@rating.get("/detail", response_model=RatingShortOut)
async def get_rating_by_pk_endpoint(
        rating_out: Annotated[RatingShortOut, Depends(RatingService.get_rating_by_pks)]
):
    return rating_out


@rating.get("/{route_id}", response_model=RatingShortOut)
async def get_my_rating_by_route_endpoint(
        rating_out: Annotated[RatingShortOut, Depends(RatingService.get_my_rating_by_route)]
):
    return rating_out


@rating.get("/avg/{route_id}", response_model=RatingAvgValue)
async def get_avg_rating_by_route_endpoint(
        rating_out: Annotated[RatingAvgValue, Depends(RatingService.get_avg_rating_by_route)]
):
    return rating_out


@rating.post("/", response_model=RatingShortOut)
async def create_rating_endpoint(
        rating_out: Annotated[RatingShortOut, Depends(RatingService.create_rating)]
):
    return rating_out


@rating.put("/", response_model=RatingShortOut)
async def update_rating_by_id_endpoint(
        rating_out: Annotated[RatingShortOut, Depends(RatingService.update_rating_by_route)]
):
    return rating_out


@rating.delete("/")
async def delete_rating_by_id_endpoint(
        rating_out: Annotated[None, Depends(RatingService.delete_rating_by_route)]
):
    return rating_out

