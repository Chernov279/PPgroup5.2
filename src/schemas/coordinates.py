


from src.schemas.base import BaseSchema


class CoordinateBaseSchema(BaseSchema):
    @classmethod
    def get_selected_columns(cls, cls_model=...):
        pass


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