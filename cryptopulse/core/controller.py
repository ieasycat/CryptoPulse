from typing import List

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from core.models import CryptoPulse, Currency, DateRecord, TimeRecord, Exchange


class BaseController:

    @staticmethod
    async def find(session: AsyncSession, model, **kwargs) -> int | None:
        stmt = select(model).filter_by(**kwargs)
        result: model | None = await session.scalar(stmt)
        return result.id

    @staticmethod
    async def create(session: AsyncSession, model, **kwargs) -> int:
        instance = model(**kwargs)
        session.add(instance)
        await session.commit()
        return instance.id

    @classmethod
    async def find_or_create(cls, session: AsyncSession, model, **kwargs) -> int:
        result = await cls.find(session=session, model=model, **kwargs)

        if not result:
            result = await cls.create(session=session, model=model, **kwargs)

        return result


class CryptoPulseController:

    @staticmethod
    async def list_cryptopulses(session: AsyncSession) -> List[CryptoPulse]:
        stmt = (
            select(CryptoPulse)
            .options(
                joinedload(CryptoPulse.currency),
                joinedload(CryptoPulse.date),
                joinedload(CryptoPulse.time),
                joinedload(CryptoPulse.exchange),
            )
            .join(CryptoPulse.currency)
            .filter_by(activated=True)
            .order_by(CryptoPulse.id)
        )
        result = await session.execute(stmt)
        cryptopulses = result.scalars().all()
        return cryptopulses

    @staticmethod
    async def get_cryptopulse(
        session: AsyncSession, cryptopulse_id: int
    ) -> CryptoPulse | None:
        stmt = (
            select(CryptoPulse)
            .options(
                joinedload(CryptoPulse.currency),
                joinedload(CryptoPulse.date),
                joinedload(CryptoPulse.time),
                joinedload(CryptoPulse.exchange),
            )
            .filter_by(id=cryptopulse_id)
        )
        cryptopulse: CryptoPulse | None = await session.scalar(stmt)
        return cryptopulse

    @staticmethod
    async def create(session: AsyncSession, **kwargs) -> int:
        cryptopulse = CryptoPulse(**kwargs)
        session.add(cryptopulse)
        await session.commit()
        return cryptopulse.id


class CurrencyController(BaseController):

    @staticmethod
    async def upsert_or_create(session: AsyncSession, currencyes: list):
        stmt = insert(Currency).values(currencyes)
        stmt = stmt.on_conflict_do_update(
            index_elements=["name"],
            set_={
                "activated": True,
            },
        )
        await session.execute(stmt)
        await session.commit()

    @staticmethod
    async def find(session: AsyncSession, model, **kwargs) -> int | None:
        return await super().find(session=session, model=Currency, **kwargs)

    @classmethod
    async def find_or_create(cls, session: AsyncSession, **kwargs) -> int:
        return await super().find_or_create(session=session, model=Currency, **kwargs)


class DateController(BaseController):
    @classmethod
    async def find_or_create(cls, session: AsyncSession, **kwargs) -> int:
        return await super().find_or_create(session=session, model=DateRecord, **kwargs)


class TimeController(BaseController):
    @classmethod
    async def find_or_create(cls, session: AsyncSession, **kwargs) -> int:
        return await super().find_or_create(session=session, model=TimeRecord, **kwargs)


class ExchangeController(BaseController):
    @classmethod
    async def find_or_create(cls, session: AsyncSession, **kwargs) -> int:
        return await super().find_or_create(session=session, model=Exchange, **kwargs)
