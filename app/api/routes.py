"""Version 1 banking API routes."""

import json
from typing import Annotated, List, Any

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.account import AccountCreate, AccountResponse, BalanceResponse
from app.schemas.customer import CustomerCreate, CustomerResponse
from app.schemas.transaction import TransactionCreate, TransactionResponse
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.account_service import AccountService
from app.services.customer_service import CustomerService
from app.services.transaction_service import TransactionService
from app.agents.dependencies import get_banking_agent

router = APIRouter(prefix="/api/v1")
DbSession = Annotated[Session, Depends(get_db)]
BankingAgent = Annotated[Any, Depends(get_banking_agent)]


@router.post("/customers", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
def create_customer(payload: CustomerCreate, db: DbSession) -> CustomerResponse:
    """Register a new customer."""

    return CustomerResponse.model_validate(CustomerService(db).create(payload))


@router.get("/customers/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: int, db: DbSession) -> CustomerResponse:
    """Retrieve customer information."""

    return CustomerResponse.model_validate(CustomerService(db).get(customer_id))

@router.get("/customers/{customer_id}/accounts")
def get_customer_accounts(customer_id: int, db: DbSession) -> List[AccountResponse]:
    """Gets account no linked to a specific customer"""
    return AccountService(db).get_customer_account(customer_id)

@router.post("/customers/{customer_id}/accounts", response_model=AccountResponse, status_code=status.HTTP_201_CREATED)
def create_account(customer_id: int, payload: AccountCreate, db: DbSession) -> AccountResponse:
    """Open an account for an existing customer."""

    return AccountResponse.model_validate(AccountService(db).create(customer_id, payload))


@router.post("/accounts", response_model=AccountResponse, status_code=status.HTTP_201_CREATED)
def create_account_legacy(payload: AccountCreate, db: DbSession) -> AccountResponse:
    """Compatibility endpoint for the original account API."""

    return AccountResponse.model_validate(AccountService(db).create(payload.customer_id, payload))


@router.get("/customers/{customer_id}/accounts/{account_number}", response_model=AccountResponse)
def get_account(customer_id: int, account_number: str, db: DbSession) -> AccountResponse:
    """Retrieve account information."""

    return AccountResponse.model_validate(AccountService(db).get(customer_id, account_number))


@router.get("/customers/{customer_id}/accounts/{account_number}/balance", response_model=BalanceResponse)
def get_balance(customer_id: int, account_number: str, db: DbSession) -> BalanceResponse:
    """Retrieve the current account balance."""

    return AccountService(db).get_balance(customer_id, account_number)


@router.get("/accounts/{account_number}/balance", response_model=BalanceResponse)
def get_balance_legacy(account_number: str, db: DbSession) -> BalanceResponse:
    """Compatibility endpoint for the original account API."""

    return AccountService(db).get_balance(account_number)


@router.post(
    "/customers/{customer_id}/accounts/{account_number}/transactions",
    response_model=TransactionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_transaction(
    customer_id: int, account_number: str, payload: TransactionCreate, db: DbSession
) -> TransactionResponse:
    """Post a credit or debit transaction."""

    return TransactionResponse.model_validate(
        TransactionService(db).create(customer_id, account_number, payload)
    )


@router.post(
    "/accounts/{account_number}/transactions",
    response_model=TransactionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_transaction_legacy(
    account_number: str, payload: TransactionCreate, db: DbSession
) -> TransactionResponse:
    """Compatibility endpoint for the original account API."""

    account = AccountService(db).get(account_number)
    return TransactionResponse.model_validate(
        TransactionService(db).create(account.customer_id, account_number, payload)
    )


@router.get(
    "/customers/{customer_id}/accounts/{account_number}/transactions", response_model=list[TransactionResponse]
)
def list_transactions(
    customer_id: int,
    account_number: str,
    db: DbSession,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> list[TransactionResponse]:
    """Retrieve paginated transaction history."""

    transactions = TransactionService(db).list_for_account(customer_id, account_number, limit, offset)
    return [TransactionResponse.model_validate(transaction) for transaction in transactions]


@router.get(
    "/accounts/{account_number}/transactions", response_model=list[TransactionResponse]
)
def list_transactions_legacy(
    account_number: str,
    db: DbSession,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> list[TransactionResponse]:
    """Compatibility endpoint for the original account API."""

    account = AccountService(db).get(account_number)
    transactions = TransactionService(db).list_for_account(
        account.customer_id, account_number, limit, offset
    )
    return [TransactionResponse.model_validate(transaction) for transaction in transactions]


@router.post("/chat", response_model=ChatResponse)
def chat(
    payload: ChatRequest,
    agent: BankingAgent,
):
    result = agent.invoke(
        {"messages": [{"role": "user", "content": payload.message}]},
        config={
            "run_name": "banking-chat",
            "tags": ["banking-agent"],
            "metadata": {
                "environment": "development",
                "agent_version": "v1",
            },
        },
    )

    return ChatResponse(
        response=result["messages"][-1].content,
        account_options=_account_options_from_tool_result(result["messages"]),
    )


def _account_options_from_tool_result(messages: list[Any]) -> list[AccountResponse]:
    """Expose account-list tool results as typed UI data, when the agent used that tool."""

    for message in reversed(messages):
        if getattr(message, "name", None) != "get_customer_accounts":
            continue
        content = message.content
        if isinstance(content, str):
            try:
                content = json.loads(content)
            except json.JSONDecodeError:
                return []
        if not isinstance(content, list):
            return []
        try:
            return [AccountResponse.model_validate(account) for account in content]
        except (TypeError, ValueError):
            return []
    return []
