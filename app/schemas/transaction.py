"""Transaction API schemas."""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.models.transaction import TransactionType


class TransactionCreate(BaseModel):
    """Fields required to post a transaction."""

    transaction_type: TransactionType
    amount: Decimal = Field(gt=0, max_digits=19, decimal_places=2)
    description: str | None = Field(default=None, max_length=255)


class TransactionResponse(BaseModel):
    """A posted account transaction."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    account_id: int
    transaction_type: TransactionType
    amount: Decimal
    description: str | None
    reference: str
    created_at: datetime

