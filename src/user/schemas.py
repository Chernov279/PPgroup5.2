import datetime

from pydantic import BaseModel


class UserCreateIn(BaseModel):
    name: str
    email: str
    hashed_password: str

    class Config:
        from_attributes = True


class UserUpdateIn(BaseModel):
    name: str
    surname: str
    patronymic: str
    location: str
    sex: str
    birth: str

    class Config:
        from_attributes = True


class UserOut(BaseModel):
    name: str
    surname: str | None
    location: str | None
    sex: str | None
    authorized_time: datetime.datetime | None
    birth: str | None

    class Config:
        from_attributes = True
