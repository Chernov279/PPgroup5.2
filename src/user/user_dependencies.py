from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import db_helper
from .user_repository import UserRepository
from .user_uow import UserUnitOfWork


def get_user_repository(db_session: AsyncSession = Depends(db_helper.get_db_session)):
    return UserRepository(db_session)


def get_user_uow(db_session: AsyncSession = Depends(db_helper.get_db_session)):
    return UserUnitOfWork(db_session)
