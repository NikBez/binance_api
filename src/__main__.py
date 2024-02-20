import asyncio

from src.database.database import db
from src.manager import Manager
from src.telegram.bot import TelegramHandler


async def main():
    await db.init_models()
    manager = Manager()
    tasks = [
        manager.run(),
        TelegramHandler.run()
    ]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
