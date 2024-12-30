from pydantic import BaseModel


class UserLoginIn(BaseModel):
    email: str
    password: str

    class Config:
        from_attributes = True


class UserAuthIn(UserLoginIn):
    name: str


class AccessTokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

    class Config:
        from_attributes = True


class TokensOut(BaseModel):
    access_token: str
    refresh_token: str = ""
    token_type: str = "bearer"


class UserAuthOut(BaseModel):
    email: str
    name: str
    refresh_token: str
    token_type: str

    class Config:
        from_attributes = True
