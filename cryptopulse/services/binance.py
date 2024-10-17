from services.base import BaseCrypto


class BinanceInfo(BaseCrypto):
    def __init__(self, session):
        super().__init__(session=session)
        self.exchange = "Binance"
        self.api_url = {
            "openInterest": "https://fapi.binance.com/fapi/v1/openInterest?symbol=",
            "ticker24hr": "https://fapi.binance.com/fapi/v1/ticker/24hr?symbol=",
        }

    async def get_open_interest(self, currency: str) -> str:
        api_url = f"{self.api_url['openInterest']}{currency}USDT"
        result = await self.fetch_data(api_url=api_url)
        return result["openInterest"]

    async def get_ticker24(self, currency: str) -> str:
        api_url = f"{self.api_url['ticker24hr']}{currency}USDT"
        result = await self.fetch_data(api_url=api_url)
        return result["highPrice"]
