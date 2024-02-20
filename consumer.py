import asyncio

import aio_pika, sys, os
from aio_pika.abc import AbstractIncomingMessage

from src.database.database import DBHandler


async def main():
    db = DBHandler()
    await db.init_models()
    connection = await aio_pika.connect_robust(
        "amqp://guest:guest@127.0.0.1/",
    )
    async with connection:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=10)
        queue = await channel.declare_queue('hell', auto_delete=True)
        await queue.consume(on_message)
        await asyncio.Future()

async def on_message(message: AbstractIncomingMessage) -> None:
    async with message.process():
        print(f"[x] {message.body!r}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
