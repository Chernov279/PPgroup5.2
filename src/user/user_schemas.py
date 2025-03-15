import datetime

from ..models.models import User
from ..schemas.base_schemas import BaseSchema


class UserBaseSchema(BaseSchema):
    @classmethod
    def get_selected_columns(cls, cls_model=User):
        return super().get_selected_columns(cls_model)


class UserCreateIn(UserBaseSchema):
    name: str
    email: str
    hashed_password: str


class UserUpdateIn(UserBaseSchema):
    surname: str | None = None
    patronymic: str | None = None
    location: str | None = None
    sex: str | None = None
    birth: str | None = None


class UserUpdateInternal(UserUpdateIn):
    id: int


class UserShortOut(UserBaseSchema):
    id: int
    name: str
    location: str | None


class UserDetailOut(UserShortOut):
    surname: str | None
    sex: str | None
    created_at: datetime.datetime | None
    birth: str | None
