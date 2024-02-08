import asyncio
from time import sleep

from src.binance_connector import APIClient
from src.common.dependeny_manager import DependencyManager
from src.producer import run
from src.settings import SETTINGS


async def main():
    api = SETTINGS.BINANCE_API.get_secret_value()
    secret = SETTINGS.BINANCE_SECRET.get_secret_value()
    client = APIClient(api, secret, True)
    dependency_manager = DependencyManager()
    while True:
        await run(client, dependency_manager)
        sleep(5)


if __name__ == "__main__":
    asyncio.run(main())
