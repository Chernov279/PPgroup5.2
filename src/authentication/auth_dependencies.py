from .auth_uow import AuthUnitOfWork
from src.config import db_helper


async def get_auth_uow():
    async with db_helper.get_db_session() as session:
        yield AuthUnitOfWork(session)

