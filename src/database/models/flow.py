from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func, ForeignKey, DateTime

from src.database.models.base import Base


class Flow(Base):
    __tablename__ = 'flows'

    pair: Mapped[str]
    platform: Mapped[int] = mapped_column(ForeignKey("trading_platforms.id"))
    server_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    broker_time: Mapped[datetime | None]
    price: Mapped[float]
