from .route_uow import RouteUnitOfWork
from ..config import db_helper


async def get_route_uow():
    async with db_helper.get_db_session() as db_session:
        yield RouteUnitOfWork(db_session)
