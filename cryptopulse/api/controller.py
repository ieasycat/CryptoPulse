from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from core.models import CryptoPulse


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
