import datetime

from ..schemas.base_schemas import BaseSchema


class UserCreateIn(BaseSchema):
    name: str
    email: str
    hashed_password: str


class UserUpdateIn(BaseSchema):
    name: str | None = None
    surname: str | None = None
    patronymic: str | None = None
    location: str | None = None
    sex: str | None = None
    birth: str | None = None


class UserUpdateInternal(UserUpdateIn):
    id: int


class UserShortOut(BaseSchema):
    id: int
    name: str
    location: str | None


class UserDetailOut(UserShortOut):
    surname: str | None
    sex: str | None
    authorized_time: datetime.datetime | None
    birth: str | None
