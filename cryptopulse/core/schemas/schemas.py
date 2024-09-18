from datetime import date, time

from pydantic import BaseModel


class CryptoCurrencySchema(BaseModel):
    name: str
    max_price: float
    open_interest: float


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
