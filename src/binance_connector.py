from pprint import pprint
from src.settings import SETTINGS
from binance.spot import Spot


class APIClient:
    def __init__(self, api_key: str, secret: str, testmode: bool = True):
        self.__api_key = api_key
        self.__secret_key = secret
        self._client = Spot(api_key=api_key, api_secret=secret, show_limit_usage=True)
        self._testmode = testmode
        if testmode:
            self._client.base_url = SETTINGS.BINANCE_TESTNET_BASE_URL

    @property
    async def api_key(self):
        return self.__api_key

    @property
    async def secret_key(self):
        return self.__secret_key

    async def test_get_time(self):
        """
        Get server timestamp
        """
        print(self._client.time())

    async def test_get_klines(self):
        """
        Get last 10 klines of BNBUSDT at 1h interval
        """
        print(self._client.klines("BNBUSDT", "1h", limit=10))

    #
    async def test_get_account(self):
        """
        Get account and balance information
        """
        pprint(self._client.account())

    async def test_exchange_info(self):
        """
        Get account and balance information
        """
        pprint(self._client.exchange_info(), indent=2)

    async def test_book_ticker(self, symbol: str):
        """
        Get account and balance information
        """
        return self._client.book_ticker(symbol)
