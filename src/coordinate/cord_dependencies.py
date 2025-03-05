from src.config import db_helper

from .cord_uow import CoordinateUnitOfWork


async def get_coordinate_uow():
    async with db_helper.get_db_session() as db_session:
        yield CoordinateUnitOfWork(db_session)
