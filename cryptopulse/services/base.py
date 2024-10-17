from typing import TypeVar, Callable, Any

import aiohttp

import datetime as dt

from sqlalchemy.ext.asyncio import AsyncSession

from core.controller import (
    CurrencyController,
    DateController,
    TimeController,
    ExchangeController,
    CryptoPulseController,
)
from core.models import db_helper
from core.config import settings


class BaseCrypto:
    T = TypeVar("T")

    def __init__(self, session: aiohttp.ClientSession):
        self.currency_controller = CurrencyController()
        self.date_controller = DateController()
        self.time_controller = TimeController()
        self.exchange_controller = ExchangeController()
        self.cryptopulse_controller = CryptoPulseController()
        self.session = session
        self.bringx_coins_api = settings.bringx_api_url
        self.binance_coins_api = settings.binance_api_url
        self.date_now = dt.datetime.now(dt.UTC)
        self.time_now = dt.time(self.date_now.hour, self.date_now.minute)
        self.exchange = None
        self.api_url = None
        self.headers = None
        self.currencies = None

    async def initialize(self):
        self.currencies = await self.with_db_session(
            self.currency_controller.list_currencies
        )

    async def find_or_create_date_and_time(self):
        date = await self.with_db_session(
            self.date_controller.find_or_create, date=self.date_now.date()
        )
        time = await self.with_db_session(
            self.time_controller.find_or_create, time=self.time_now
        )
        return date, time

    @staticmethod
    async def with_db_session(
        func: Callable[[AsyncSession], T], *args: Any, **kwargs: Any
    ) -> T:
        async for session in db_helper.session_getter():
            return await func(session, *args, **kwargs)

    async def get_bringx_currencies(self) -> set:
        currencies = await self.fetch_data(api_url=self.bringx_coins_api)
        return {currency["asset"] for currency in currencies["data"]}

    async def get_binance_currencies(self) -> set:
        currencies = await self.fetch_data(api_url=self.binance_coins_api)
        return {
            currency["baseAsset"]
            for currency in currencies["symbols"]
            if currency["status"] == "TRADING"
        }

    async def find_common_currencies(self) -> set:
        result = (
            await self.get_bringx_currencies() & await self.get_binance_currencies()
        )
        return result

    async def create_currencies_in_db(self):
        currencies = await self.find_common_currencies()
        currencies = [{"name": currency} for currency in currencies]

        await self.with_db_session(
            self.currency_controller.upsert_or_create,
            currencies=currencies,
        )

    async def fetch_data(
        self,
        api_url: str,
    ) -> dict:
        async with self.session.get(url=api_url, headers=self.headers) as result:
            result.raise_for_status()
            return await result.json()

    async def close(self):
        if self.session:
            await self.session.close()

    async def get_open_interest(self, currency: str) -> Any:
        raise NotImplementedError("This method should be overridden in subclasses")

    async def get_ticker24(self, currency: str) -> Any:
        raise NotImplementedError("This method should be overridden in subclasses")

    async def main(
        self,
    ) -> None:
        await self.initialize()

        date, time = await self.find_or_create_date_and_time()
        exchange = await self.with_db_session(
            self.exchange_controller.find_or_create,
            name=self.exchange,
        )
        for currency in self.currencies:
            currency = currency.name
            open_interest = await self.get_open_interest(currency=currency)
            ticker24 = await self.get_ticker24(currency=currency)
            currency_for_db = await self.with_db_session(
                self.currency_controller.find,
                name=currency,
            )
            await self.with_db_session(
                self.cryptopulse_controller.create,
                currency_id=currency_for_db,
                date_id=date,
                time_id=time,
                exchange_id=exchange,
                max_price=ticker24,
                open_interest=open_interest,
            )


# пример a and b
# {'openInterest': '2848943.07', 'symbol': 'EOS-USDT', 'time': 1724000323276}
# {'openInterest': '2849602.58', 'symbol': 'EOS-USDT', 'time': 1724000468260}
# {"openInterest": "3230241.56", "symbol": "EOS-USDT", "time": 1724277115450}

# формула для получение % изменение ОИ
#  a < b = ((b-a)/a) * 100 --> %
#  a > b = ((a-b)/a) * 100 --> -%
