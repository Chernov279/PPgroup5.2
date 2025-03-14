from src.config import db_helper
from src.rating_route.rat_uow import RatingUnitOfWork


async def get_rating_uow():
    async with db_helper.get_db_session() as db_session:
        yield RatingUnitOfWork(db_session)
