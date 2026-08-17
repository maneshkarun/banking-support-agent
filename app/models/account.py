"""Bank account database model."""

from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, ForeignKey, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.customer import Customer
    from app.models.transaction import Transaction


class AccountType(StrEnum):
    """Supported bank account types."""

    SAVINGS = "savings"
    CHECKING = "checking"


class AccountStatus(StrEnum):
    """Supported account lifecycle states."""

    ACTIVE = "active"
    FROZEN = "frozen"
    CLOSED = "closed"


class Account(Base):
    """A customer's bank account and its current balance."""

    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(primary_key=True)
    account_number: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), index=True)
    account_type: Mapped[AccountType] = mapped_column(Enum(AccountType), nullable=False)
    status: Mapped[AccountStatus] = mapped_column(
        Enum(AccountStatus), default=AccountStatus.ACTIVE, nullable=False
    )
    currency: Mapped[str] = mapped_column(String(3), default="INR", nullable=False)
    balance: Mapped[Decimal] = mapped_column(Numeric(19, 2), default=Decimal("0.00"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    customer: Mapped["Customer"] = relationship(back_populates="accounts")
    transactions: Mapped[list["Transaction"]] = relationship(
        back_populates="account", cascade="all, delete-orphan"
    )
