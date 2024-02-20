
import aio_pika
from sqlalchemy import select
from src.database.database import db
import json
from src.database.models import Pair, TradingPlatform
from src.settings import SETTINGS
from src.telegram.schemas import RequestSchema, ResponseSchema


class TelegramHandler:
    @staticmethod
    async def run():
        connection = await aio_pika.connect_robust(SETTINGS.RABBITMQ_URL)
        async with connection:
            channel = await connection.channel()
            telegram_queue = await channel.declare_queue(SETTINGS.TELEGRAM_QUEUE_NAME)
            async for message in telegram_queue:
                result = message.body.decode()
                if result:
                    try:
                        message_data = json.loads(result)
                        request = RequestSchema(**message_data)
                        await TelegramHandler.handle_request(request)
                    except json.JSONDecodeError:
                        print("Received message is not valid JSON:", result)
                else:
                    print("Received an empty message from Telegram queue.")
                await message.ack()

    @staticmethod
    async def handle_request(request: RequestSchema):
        session = db.AsyncSessionLocal
        answer_text = ''
        async with (session() as session):
            if request.command in ('active_pairs', '/active_pairs'):
                active_pairs_query = select(
                    Pair.id,
                    Pair.symbol,
                    Pair.strategy,
                    TradingPlatform.title
                ).where(Pair.is_activated)
                active_pairs = (await session.execute(active_pairs_query)).all()
                for pair in active_pairs:
                    answer_text += f'- {pair._mapping['symbol']} на платформе {pair._mapping['title']}\n'
        if answer_text:
            answer = ResponseSchema(chat_id=request.chat_id, text=answer_text).model_dump()
            await TelegramHandler.send_message(answer)
        else:
            answer_text = 'Не понимаю'
            answer = ResponseSchema(chat_id=request.chat_id, text=answer_text).model_dump()
            await TelegramHandler.send_message(answer)



    @staticmethod
    async def send_message(response: dict):
        connection = await aio_pika.connect_robust(SETTINGS.RABBITMQ_URL)
        async with connection:
            channel = await connection.channel()
            queue = await channel.declare_queue(SETTINGS.SERVER_QUEUE_NAME)
            await channel.default_exchange.publish(
                aio_pika.Message(body=json.dumps(response).encode()),
                routing_key=queue.name
            )
