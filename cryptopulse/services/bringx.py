from services.base import BaseCrypto


class BringxInfo(BaseCrypto):
    def __init__(self, session):
        super().__init__(session=session)
        self.exchange = "BringX"
        self.api_url = {
            "openInterest": "https://open-api.bingx.com/openApi/swap/v2/quote/openInterest?symbol=",
            "ticker24hr": "https://open-api.bingx.com/openApi/swap/v2/quote/ticker?symbol=",
        }

    async def get_open_interest(self, currency: str) -> str:
        api_url = f"{self.api_url['openInterest']}{currency}-USDT"
        result = await self.fetch_data(api_url=api_url)
        return result["data"]["openInterest"]

    async def get_ticker24(self, currency: str) -> str:
        api_url = f"{self.api_url['ticker24hr']}{currency}-USDT"
        result = await self.fetch_data(api_url=api_url)
        return result["data"]["highPrice"]
