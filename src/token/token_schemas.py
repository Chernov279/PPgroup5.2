from src.schemas.base_schemas import BaseSchema


class FormDataInternal(BaseSchema):
    email: str
    hashed_password: str


class AccessTokenOut(BaseSchema):
    access_token: str
    token_type: str = "bearer"
