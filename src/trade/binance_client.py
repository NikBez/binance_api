from pprint import pprint

from binance.error import ClientError
from sqlalchemy import select, and_

from src.database.database import db
from src.database.models import Pair
from src.settings import SETTINGS
from binance.spot import Spot

from src.trade.base import BaseClient


class BinanceAPIClient(BaseClient):
    def __init__(self, scheduler, client_id, title, pair_price_default_periodicy: int = 60, testmode=True):
        super().__init__(scheduler, client_id, title, testmode)
        self.pair_price_default_periodicy = pair_price_default_periodicy
        self.__api_key = SETTINGS.BINANCE_API.get_secret_value()
        self.__secret_key = SETTINGS.BINANCE_SECRET.get_secret_value()
        self._client = Spot(api_key=self.__api_key, api_secret=self.__secret_key, show_limit_usage=True)
        if self.testmode:
            self._client.base_url = SETTINGS.BINANCE_TESTNET_BASE_URL

        
    async def run(self):
        session = db.AsyncSessionLocal
        async with session() as session:
            pairs_query = select(Pair.symbol, Pair.platform).where(
                and_(Pair.is_activated, Pair.platform == self.client_id))
            pairs_ = (await session.execute(pairs_query)).all()

            pairs = [r._asdict() for r in pairs_]
            has_active_pairs = self.scheduler.get_job(f'get_pair_price_{self.title}')
            if pairs:
                if not has_active_pairs:
                    self.scheduler.add_job(self.get_pair_price, 'interval', seconds=self.pair_price_default_periodicy,
                                      id=f'get_pair_price_{self.title}',
                                      args=(pairs,))
                else:
                    self.scheduler.modify_job(f'get_pair_price_{self.title}',
                                         args=(pairs,))
            elif not pairs and has_active_pairs:
                self.scheduler.remove_job(f'get_pair_price_{self.title}')


    async def get_pair_price(self, pairs: list[dict]):
        try:
            price_data = self._client.book_ticker(symbols=[r['symbol'] for r in pairs])
            print(price_data['limit_usage']['x-mbx-used-weight-1m'])
            await self.add_pair_price(price_data)
        except ClientError as err:
            print(err.error_message)
    
    
    @property
    async def api_key(self):
        return self.__api_key

    @property
    async def secret_key(self):
        return self.__secret_key


