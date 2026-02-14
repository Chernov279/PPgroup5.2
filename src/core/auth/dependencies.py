from typing import Optional

from fastapi import Body, Cookie, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from src.db.db_helper import get_db_session

from .service import AuthService
from .utils.token_utils import get_sub_from_token


async def get_auth_service(
    session: AsyncSession = Depends(get_db_session),
) -> AuthService:
    return AuthService(session)
