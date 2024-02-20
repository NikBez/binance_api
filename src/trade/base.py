
from pydantic import ValidationError

from src.database.database import db
from src.database.models import Flow
from src.schemas import FlowSchema


class BaseClient:
    def __init__(self, scheduler, client_id, title, testmode: bool = True):
        self.client_id = client_id
        self.title = title
        self.testmode = testmode
        self.scheduler = scheduler


    async def add_pair_price(self, price_data: dict):
        session = db.AsyncSessionLocal
        async with session() as session:
            for pair in price_data['data']:
                pair_data = {
                    'pair': pair['symbol'],
                    'platform': self.client_id,
                    'price': pair['bidPrice'],
                }
                try:
                    flow_data = FlowSchema(**pair_data)
                except ValidationError as e:
                    print(f"Ошибка валидации: {e}")
                    continue
                new_flow = Flow(**flow_data.model_dump())
                session.add(new_flow)
            await session.commit()
