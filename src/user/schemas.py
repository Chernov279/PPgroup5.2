from pydantic import BaseModel


class UserOut(BaseModel):
    name: str
    surname: str | None
    location: str | None
    sex: str | None
    authorized_time: str | None
    birth: str | None

    class Config:
        from_attributes = True
