from typing import Optional

from fastapi import Body, Cookie

from src.config import db_helper
from .service import AuthService


async def get_auth_service():
    async with db_helper.get_db_session() as db_session:
        yield AuthService(db_session)


async def get_refresh_token(
    refresh_token: Optional[str] = Body(None, embed=True),
    refresh_token_cookie: Optional[str] = Cookie(None, alias="refresh_token")
) -> str:
    token = refresh_token_cookie or refresh_token
    return token