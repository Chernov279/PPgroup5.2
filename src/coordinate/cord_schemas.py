from ..schemas.base_schemas import BaseSchema


class CordOut(BaseSchema):
    route_id: int
    user_id: int
    order: int | None = None
    latitude: float
    longitude: float


class CoordinatesIn(BaseSchema):
    latitude: float
    longitude: float


class CoordinatesInDB(BaseSchema):
    user_id: int
    route_id: int | None = None
    order: int | None = None
    latitude: float
    longitude: float

    def __str__(self):
        return (f"user_id={self.user_id},"
                f"route_id={self.route_id},"
                f"order={self.order},"
                f"latitude={self.latitude},"
                f"longitude={self.longitude}")