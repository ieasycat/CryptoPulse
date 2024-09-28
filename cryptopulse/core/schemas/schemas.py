from datetime import date, time

from decimal import Decimal

from pydantic import BaseModel


class CryptoCurrencySchema(BaseModel):
    name: str


class DateSchema(BaseModel):
    date: date


class TimeSchema(BaseModel):
    time: time


class ExchangeSchema(BaseModel):
    name: str


class CryptoPulseSchema(BaseModel):
    id: int
    currency: CryptoCurrencySchema
    date: DateSchema
    time: TimeSchema
    exchange: ExchangeSchema
    max_price: Decimal
    open_interest: Decimal
