import asyncio

import aiohttp

from services.base import BaseCrypto
from services.bringx import BringxInfo
from services.binance import BinanceInfo

from time import time as t


async def main():
    session = aiohttp.ClientSession()

    base = BaseCrypto(session=session)
    await base.find_or_create_date_and_time()

    bringx = BringxInfo(session=session)
    binance = BinanceInfo(session=session)

    st = t()

    await base.create_currencies_in_db()

    await asyncio.gather(bringx.main(), binance.main())

    f = t()

    print(f - st)

    await base.close()


if __name__ == "__main__":
    asyncio.run(main())
