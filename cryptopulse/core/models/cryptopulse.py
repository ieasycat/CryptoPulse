import datetime

from sqlalchemy import ForeignKey, DECIMAL
from sqlalchemy.dialects.postgresql import DATE, TIME
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from core.models import Base
from core.models.mixins import CryptoDataMixin


class Currency(CryptoDataMixin, Base):
    _cryptopulse_back_populates = "currency"

    name: Mapped[str] = mapped_column(unique=True, index=True)
    activated: Mapped[bool] = mapped_column(default=True)


class DateRecord(CryptoDataMixin, Base):
    _cryptopulse_back_populates = "date"

    date: Mapped[datetime.date] = mapped_column(
        DATE,
        unique=True,
        server_default=func.current_date(),
    )


class TimeRecord(CryptoDataMixin, Base):
    _cryptopulse_back_populates = "time"

    time: Mapped[datetime.time] = mapped_column(TIME)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        time = datetime.datetime.now(datetime.UTC).time()
        self.time = datetime.time(hour=time.hour, minute=time.minute)


class Exchange(CryptoDataMixin, Base):
    _cryptopulse_back_populates = "exchange"

    name: Mapped[str] = mapped_column(unique=True)


class CryptoPulse(Base):
    currency_id: Mapped[int] = mapped_column(ForeignKey(Currency.id))
    date_id: Mapped[int] = mapped_column(ForeignKey(DateRecord.id))
    time_id: Mapped[int] = mapped_column(ForeignKey(TimeRecord.id))
    exchange_id: Mapped[int] = mapped_column(ForeignKey(Exchange.id))

    max_price: Mapped[DECIMAL] = mapped_column(DECIMAL(precision=40, scale=5))
    open_interest: Mapped[DECIMAL] = mapped_column(DECIMAL(precision=40, scale=5))

    currency: Mapped[Currency] = relationship(back_populates="cryptopulses")
    date: Mapped[DateRecord] = relationship(back_populates="cryptopulses")
    time: Mapped[TimeRecord] = relationship(back_populates="cryptopulses")
    exchange: Mapped[Exchange] = relationship(back_populates="cryptopulses")
