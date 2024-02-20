from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from src.database.models.base import Base


class Pair(Base):
    __tablename__ = 'pairs'

    symbol: Mapped[str]
    strategy: Mapped[str | None]
    platform: Mapped[int] = mapped_column(ForeignKey('trading_platforms.id'))
    is_activated: Mapped[bool] = mapped_column(default=False)
