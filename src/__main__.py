import asyncio
from time import sleep

from src.binance_connector import APIClient
from src.producer import run
from src.settings import SETTINGS


async def main():
    api = SETTINGS.BINANCE_API.get_secret_value()
    secret = SETTINGS.BINANCE_SECRET.get_secret_value()
    client = APIClient(api, secret, True)
    while True:
        await run(client)
        sleep(5)


if __name__ == '__main__':
    asyncio.run(main())




