from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .service import UserService
from ..config.database.db_helper import get_db_session


async def get_user_service(
    session: AsyncSession = Depends(get_db_session),
) -> UserService:
    return UserService(session)
