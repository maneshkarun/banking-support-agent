"""Account API schemas."""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.models.account import AccountStatus, AccountType


class AccountCreate(BaseModel):
    """Fields required to open an account."""

    customer_id: int = Field(gt=0)
    account_type: AccountType
    currency: str = Field(default="INR", min_length=3, max_length=3, pattern=r"^[A-Z]{3}$")
    opening_balance: Decimal = Field(default=Decimal("0.00"), ge=0, decimal_places=2)


class AccountResponse(BaseModel):
    """Public account information."""

    model_config = ConfigDict(from_attributes=True)

    account_number: str
    customer_id: int
    account_type: AccountType
    status: AccountStatus
    currency: str
    balance: Decimal
    created_at: datetime


class BalanceResponse(BaseModel):
    """Current account balance response."""

    account_number: str
    currency: str
    balance: Decimal