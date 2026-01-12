import datetime
from typing import Optional, Any

from fastapi import Query

from ..models.models import User
from ..schemas.base_schemas import BaseSchema


class UserBaseSchema(BaseSchema):
    __model__ = User


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
    last_active_time: Optional[datetime.datetime]


class UserActivityInternal(UserBaseSchema):
    id: int
    last_active_time: Optional[datetime.datetime]


class UserActivityOut(UserActivityInternal):
    formatted_last_active_time: Optional[str]


class UserUpdateActivityOut(BaseSchema):
    """Схема для ответа об обновлении активности"""
    user_id: int
    last_active_time: datetime.datetime
    updated: bool
    message: str = "Activity updated"

class UserDeleteOut(BaseSchema):
    """Схема для ответа об удалении"""
    user_id: int
    message: str = "User deleted successfully"
    timestamp: datetime.datetime