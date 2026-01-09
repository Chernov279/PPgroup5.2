from typing import Optional

from fastapi import Body, Cookie, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .service import AuthService
from ..config.database.db_helper import get_db_session


async def get_auth_service(
    session: AsyncSession = Depends(get_db_session),
) -> AuthService:
    return AuthService(session)


async def get_refresh_token(
    refresh_token: Optional[str] = Body(None, embed=True),
    refresh_token_cookie: Optional[str] = Cookie(None, alias="refresh_token")
) -> str:
    token = refresh_token_cookie or refresh_token
    return token