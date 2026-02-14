from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from src.core.ratings.uow import RatingUnitOfWork
from src.db import db_helper

async def get_ratings_uow(db_session: AsyncSession = Depends(db_helper.get_db_session)):
    return RatingUnitOfWork(db_session)
