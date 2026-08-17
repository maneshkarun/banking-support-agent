"""Account transaction database model."""

from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, ForeignKey, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.account import Account


class TransactionType(StrEnum):
    """Supported transaction directions."""

    CREDIT = "credit"
    DEBIT = "debit"


class Transaction(Base):
    """An immutable credit or debit entry for an account."""

    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"), index=True)
    transaction_type: Mapped[TransactionType] = mapped_column(Enum(TransactionType))
    amount: Mapped[Decimal] = mapped_column(Numeric(19, 2), nullable=False)
    description: Mapped[str | None] = mapped_column(String(255))
    reference: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), index=True, nullable=False
    )

    account: Mapped["Account"] = relationship(back_populates="transactions")
