from fastapi import Depends
from httpx import get
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.coordinate.uow import CoordinateUnitOfWork
from src.db import db_helper

async def get_coordinate_uow(db_session: AsyncSession = Depends(db_helper.get_db_session)):
    return CoordinateUnitOfWork(db_session)
