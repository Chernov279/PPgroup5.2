from src.schemas.base_schemas import BaseSchema
import datetime


class RatingOut(BaseSchema):
    route_id: int
    user_id: int
    value: int
    created_time: datetime.datetime
    comment: str


class RatingCreateIn(BaseSchema):
    route_id: int
    value: int | None
    comment: str | None


class RatingCreateInInternal(RatingCreateIn):
    user_id: int


class RatingUpdateIn(BaseSchema):
    route_id: int
    value: int | None
    comment: str | None


class RatingUpdateInInternal(RatingUpdateIn):
    user_id: int


class RatingFK(BaseSchema):
    user_id: int
    route_id: int
