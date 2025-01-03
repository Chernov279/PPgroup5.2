import datetime
from typing import Tuple

from pydantic import BaseModel


class RouteCreateIn(BaseModel):
    distance: float | None
    users_travel_time: int | None
    users_travel_speed: int | None
    users_transport: str | None
    comment: str | None
    locname_start: str | None
    locname_finish: str | None


class RouteUpdateIn(BaseModel):
    id: int
    distance: float | None
    users_travel_time: int | None
    users_travel_speed: int | None
    users_transport: str | None
    comment: str | None
    locname_start: str | None
    locname_finish: str | None


class RouteOut(BaseModel):
    id: int
    user_id: int
    distance: float | None
    users_travel_time: int | None
    users_transport: str | None
    comment: str | None
    created_time: datetime.datetime | None
    locname_start: str | None
    locname_finish: str | None


class RouteDetailOut(BaseModel):
    id: int
    distance: float | None
    users_travel_time: int | None
    users_travel_speed: int | None
    users_transport: str | None
    comment: str | None
    created_time: datetime.datetime | None
    locname_start: str | None
    locname_finish: str | None
    user_name: str | None = None
    avg_estimation: float | None = None
    amount_estimations: int | None = 0
    start_coordinate: Tuple[float, float] | None
    finish_coordinate: Tuple[float, float] | None
    amount_points: int | None
