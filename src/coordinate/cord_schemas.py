from ..models.models import Coordinate
from ..schemas.base_schemas import BaseSchema


class CoordinateBaseSchema(BaseSchema):
    @classmethod
    def get_selected_columns(cls, cls_model=Coordinate):
        return super().get_selected_columns(cls_model)


class CoordinateOut(CoordinateBaseSchema):
    order: int | None = None
    latitude: float
    longitude: float


class CoordinateCreateIn(CoordinateBaseSchema):
    latitude: float
    longitude: float


class CoordinateInternal(CoordinateBaseSchema):
    user_id: int | None = None
    route_id: int | None = None
    order: int | None = None
    latitude: float | None = None
    longitude: float | None = None