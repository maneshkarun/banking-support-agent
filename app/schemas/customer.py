"""Customer API schemas."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.schemas.account import AccountResponse
class CustomerCreate(BaseModel):
    """Fields required to register a customer."""

    full_name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    phone: str | None = Field(default=None, max_length=30)


class CustomerResponse(BaseModel):
    """Public customer information."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    email: EmailStr
    phone: str | None
    created_at: datetime

