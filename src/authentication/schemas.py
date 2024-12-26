from pydantic import BaseModel


class UserAuthIn(BaseModel):
    email: str
    password: str
    name: str

    class Config:
        from_attributes = True


class UserAuthOut(BaseModel):
    email: str
    name: str
    refresh_token: str
    token_type: str

    class Config:
        from_attributes = True
