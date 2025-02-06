from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .token_repository import TokenRepository
from .token_uow import TokenUnitOfWork
from ..config import db_helper


def get_token_uow(db_session: AsyncSession = Depends(db_helper.get_db_session)) -> TokenUnitOfWork:
    return TokenUnitOfWork(db_session)


def get_token_repository(db_session: AsyncSession = Depends(db_helper.get_db_session)) -> TokenRepository:
    return TokenRepository(db_session)
