from datetime import datetime
from typing import Optional

from src.config import settings
from src.schemas.base import BaseSchema
from src.schemas.schemas import UserBaseSchema

TOKEN_TYPE: str = 'Bearer'


class RefreshTokenIn(BaseSchema):
    refresh_token: str


class AuthLoginIn(UserBaseSchema):
    email: str
    password: str


class AuthRegisterIn(AuthLoginIn):
    name: str


class AuthRegisterInternal(UserBaseSchema):
    email: str
    name: str
    hashed_password: str


class RefreshTokenInternal(BaseSchema):
    user_id: int
    token_hash: str
    expires_at: datetime
    device_fingerprint: Optional[str] = None
    revoked_at: Optional[datetime] = None


class TokensOut(BaseSchema):
    access_token: str
    refresh_token: str
    token_type: str = TOKEN_TYPE
    access_expires_in: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES


class AccessTokenOut(BaseSchema):
    access_token: str
    token_type: str = TOKEN_TYPE


class LogoutOut(BaseSchema):
    message: str = "Successfully logged out from device"
    device_logged_out: bool
    timestamp: str


class LogoutAllOut(BaseSchema):
    message: str = "Successfully logged out from all devices"
    devices_logged_out: int
    timestamp: str