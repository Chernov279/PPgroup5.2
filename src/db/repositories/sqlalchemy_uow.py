from sqlalchemy import Cast
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from .base_uow import BaseUnitOfWork


class SqlAlchemyUnitOfWork(BaseUnitOfWork):
    def __init__(self, session_or_factory):
        self.session_or_factory = session_or_factory
        self.session: AsyncSession

    async def __aenter__(self):
        if isinstance(self.session_or_factory, async_sessionmaker):
            self.session = self.session_or_factory()
        else:
            self.session = self.session_or_factory
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if isinstance(self.session_or_factory, async_sessionmaker):
            await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
