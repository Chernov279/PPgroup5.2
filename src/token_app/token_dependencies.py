from typing import Optional

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.requests import Request

from .token_repository import TokenRepository
from .token_uow import TokenUnitOfWork
from ..config import db_helper


async def get_token_uow():
    async with db_helper.get_db_session() as db_session:
        yield TokenUnitOfWork(db_session)


def get_token_repository(db_session: AsyncSession = Depends(db_helper.get_db_session)) -> TokenRepository:
    return TokenRepository(db_session)


async def get_optional_token(request: Request) -> Optional[str]:
    """
    Получает токен из заголовка Authorization.
    Если токена нет — просто возвращает None, без ошибки 401.
    """
    authorization: Optional[str] = request.headers.get("Authorization")
    if authorization and authorization.startswith("Bearer "):
        return authorization.split("Bearer ")[1]
    return None
