from sqlalchemy.orm import declared_attr, Mapped, relationship

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.models import CryptoPulse


class CryptoDataMixin:
    _cryptopulse_back_populates: str | None = None

    @declared_attr
    def cryptopulses(cls) -> Mapped["CryptoPulse"]:
        return relationship(
            "CryptoPulse",
            back_populates=cls._cryptopulse_back_populates,
        )
