import datetime
from typing import Tuple

from ..models.models import Route
from ..schemas.base_schemas import BaseSchema


class RouteBaseSchema(BaseSchema):
    @classmethod
    def get_selected_columns(cls, cls_model=Route):
        return super().get_selected_columns(cls_model)


class RouteCreateIn(RouteBaseSchema):
    distance: float | None = None
    users_travel_time: int | None = None
    users_travel_speed: int | None = None
    users_transport: str | None = None
    comment: str | None = None
    locname_start: str | None = None
    locname_finish: str | None = None


class RouteCreateInternal(RouteCreateIn):
    user_id: int | None = None


class RouteUpdateIn(RouteBaseSchema):
    id: int
    distance: float | None = None
    users_travel_time: int | None = None
    users_transport: str | None = None
    comment: str | None = None
    locname_start: str | None = None
    locname_finish: str | None = None


class RouteOut(RouteBaseSchema):
    id: int | None = None
    user_id: int | None = None
    distance: float | None = None
    users_travel_time: int | None = None
    users_transport: str | None = None
    comment: str | None = None
    created_time: datetime.datetime | None = None
    locname_start: str | None = None
    locname_finish: str | None = None


class RouteDetailOut(RouteOut):
    user_name: str | None = None
    avg_rating: float | None = None
    amount_ratings: int | None = 0
    amount_points: int | None = 0
