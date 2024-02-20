from datetime import datetime

from pydantic import BaseModel

class PairSchema(BaseModel):
    symbol: str
    strategy: str
    is_active: bool
    period: int


class FlowSchema(BaseModel):
    pair: str
    platform: int
    broker_time: datetime | None = None
    price: float