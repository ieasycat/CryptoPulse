from typing import List, Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from core.schemas.schemas import CryptoPulseSchema
from core.controller import CryptoPulseController

router = APIRouter()


@router.get("/", response_model=list[CryptoPulseSchema])
async def list_cryptopulses(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
) -> List[CryptoPulseSchema]:
    return await CryptoPulseController.list_cryptopulses(session=session)


@router.get("/{cryptopulse_id}/")
async def get_cryptopulse_by_id(
    cryptopulse_id: int,
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
) -> CryptoPulseSchema:
    return await CryptoPulseController.get_cryptopulse(
        session=session, cryptopulse_id=cryptopulse_id
    )
