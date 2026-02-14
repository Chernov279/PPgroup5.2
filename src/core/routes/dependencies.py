from src.core.routes.route_uow import RouteUnitOfWork
from src.db import db_helper

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

async def get_route_uow(db_session: AsyncSession = Depends(db_helper.get_db_session)):
    return RouteUnitOfWork(db_session)