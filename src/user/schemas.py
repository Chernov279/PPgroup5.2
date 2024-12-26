from pydantic import BaseModel


class UserOut(BaseModel):
    name: str
    surname: str
    location: str
    sex: str
    authorized_time: str
    birth: str

    class Config:
        from_attributes = True
