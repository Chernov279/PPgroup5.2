from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.db_helper import get_db_session

from .service import UserService


async def get_user_service(
    session: AsyncSession = Depends(get_db_session),
) -> UserService:
    return UserService(session)
