from typing import AsyncIterator

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.exc import SQLAlchemyError

from src.settings import SETTINGS
from src.database.models.base import Base


class DBHandler:
    def __init__(self):

        self.engine = create_async_engine(
            SETTINGS.DB_URL,
            pool_pre_ping=True,
            echo=SETTINGS.POSTGRES_ECHO,
        )
        self.AsyncSessionLocal = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def get_session(self) -> AsyncIterator[async_sessionmaker]:
        try:
            async_session = self.AsyncSessionLocal()
            async with async_session as session:
                yield session
        except SQLAlchemyError:
            await session.rollback()
            raise
        finally:
            await session.close()

    async def init_models(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
