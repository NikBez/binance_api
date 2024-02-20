from sqlalchemy.orm import Mapped, mapped_column

from src.database.models.base import Base


class TradingPlatform(Base):

    __tablename__ = 'trading_platforms'

    title: Mapped[str]
    is_activated: Mapped[bool] = mapped_column(default=False)
    pair_price_default_periodicy: Mapped[int] = mapped_column(default=60)
    max_weight: Mapped[int]
    testmode: Mapped[bool] = mapped_column(default=True)

