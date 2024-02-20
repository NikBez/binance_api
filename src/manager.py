import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import select

from src.database.models import TradingPlatform
from src.trade.base import BaseClient
from src.trade.binance_client import BinanceAPIClient
from src.database.database import db


class Manager:
    def __init__(self):
        self.__active_clients: dict[str, BaseClient | None] = {'binance': None, 'tinkoff': None}
        self.scheduler = AsyncIOScheduler(timezone='Europe/Moscow')


    async def run(self):
        await self.refresh_clients()
        self.scheduler.add_job(self.refresh_clients, 'interval', id='refresh_platforms', seconds=1)
        self.scheduler.start()
        try:
            await asyncio.Event().wait()
        finally:
            self.scheduler.shutdown()

    async def refresh_clients(self):
        session = db.AsyncSessionLocal
        query = select(TradingPlatform).where(TradingPlatform.is_activated)
        async with session() as session:
            platforms = (await session.scalars(query)).all()
        for platform in platforms:
            if platform.title == 'binance':
                binance_client = BinanceAPIClient(
                    self.scheduler,
                    platform.id,
                    platform.title,
                    platform.pair_price_default_periodicy,
                    platform.testmode
                )
                self.__active_clients['binance'] = binance_client
                await binance_client.run()

    @property
    async def active_platforms(self):
        return self.__active_platforms

    @active_platforms.setter
    async def active_platforms(self, platforms):
        self.__active_platforms = platforms

