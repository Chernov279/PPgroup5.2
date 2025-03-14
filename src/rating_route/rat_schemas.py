from typing import Optional

from fastapi import Query

from src.models.models import Rating
from src.schemas.base_schemas import BaseSchema
import datetime


class RatingBaseSchema(BaseSchema):
    @classmethod
    def get_selected_columns(cls, cls_model=Rating):
        return super().get_selected_columns(cls_model)


class RatingShortOut(RatingBaseSchema):
    value: int
    created_time: datetime.datetime
    comment: str | None


class RatingOut(RatingShortOut):
    route_id: int
    user_id: int


class RatingCreateIn(RatingBaseSchema):
    route_id: int
    value: int | None
    comment: str | None


class RatingCreateInInternal(RatingCreateIn):
    user_id: int


class RatingUpdateIn(RatingBaseSchema):
    route_id: int
    value: int | None
    comment: Optional[str] = None


class RatingUpdateInternal(RatingUpdateIn):
    user_id: int


class RatingPKs(RatingBaseSchema):
    user_id: int = Query(..., description="User ID")
    route_id: int = Query(..., description="Route ID")
