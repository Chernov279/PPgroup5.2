from pydantic import BaseModel


class UserLoginIn(BaseModel):
    email: str
    password: str

    class Config:
        from_attributes = True


class UserAuthIn(UserLoginIn):
    name: str


class UserLoginOut(BaseModel):
    refresh_token: str
    token_type: str = "bearer"

    class Config:
        from_attributes = True


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

    class Config:
        from_attributes = True


class UserAuthOut(BaseModel):
    email: str
    name: str
    refresh_token: str
    token_type: str

    class Config:
        from_attributes = True
