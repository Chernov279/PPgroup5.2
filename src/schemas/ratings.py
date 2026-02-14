from typing import Optional

from fastapi import Query

import datetime

from src.schemas.base import BaseSchema


class RatingBaseSchema(BaseSchema):
    @classmethod
    def get_selected_columns(cls, cls_model=...):
        pass


class RatingShortOut(RatingBaseSchema):
    value: int
    created_at: datetime.datetime
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


class RatingUpdateIn(RatingCreateIn):
    pass


class RatingUpdateInternal(RatingUpdateIn):
    user_id: int


class RatingPKs(RatingBaseSchema):
    user_id: int = Query(..., description="User ID")
    route_id: int = Query(..., description="Route ID")


class RatingAvgValue(RatingBaseSchema):
    value: Optional[float]
