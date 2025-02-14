from src.user.user_schemas import UserBaseSchema


class AuthLoginIn(UserBaseSchema):
    email: str
    password: str


class AuthRegisterIn(AuthLoginIn):
    name: str


class AuthRegisterInternal(UserBaseSchema):
    email: str
    name: str
    hashed_password: str
