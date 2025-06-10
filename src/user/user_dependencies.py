from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import db_helper
from .user_repository import UserRepository
from .user_uow import UserUnitOfWork


def get_user_repo_sync(db_session: AsyncSession = Depends(db_helper.get_db_session)):
    return UserRepository(db_session)


async def get_user_uow():
    async with db_helper.get_db_session() as db_session:
        yield UserUnitOfWork(db_session)


async def get_user_repo():
    async with db_helper.get_db_session() as db_session:
        yield UserRepository(db_session)
