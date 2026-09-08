from pydantic import BaseModel, Field

from app.schemas.account import AccountResponse

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    account_options: list[AccountResponse] = Field(default_factory=list)
