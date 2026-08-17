"""Version 1 banking API routes."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.account import AccountCreate, AccountResponse, BalanceResponse
from app.schemas.customer import CustomerCreate, CustomerResponse
from app.schemas.transaction import TransactionCreate, TransactionResponse
from app.services.account_service import AccountService
from app.services.customer_service import CustomerService
from app.services.transaction_service import TransactionService

router = APIRouter(prefix="/api/v1")
DbSession = Annotated[Session, Depends(get_db)]


@router.post("/customers", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
def create_customer(payload: CustomerCreate, db: DbSession) -> CustomerResponse:
    """Register a new customer."""

    return CustomerResponse.model_validate(CustomerService(db).create(payload))


@router.get("/customers/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: int, db: DbSession) -> CustomerResponse:
    """Retrieve customer information."""

    return CustomerResponse.model_validate(CustomerService(db).get(customer_id))


@router.post("/accounts", response_model=AccountResponse, status_code=status.HTTP_201_CREATED)
def create_account(payload: AccountCreate, db: DbSession) -> AccountResponse:
    """Open an account for an existing customer."""

    return AccountResponse.model_validate(AccountService(db).create(payload))


@router.get("/accounts/{account_number}", response_model=AccountResponse)
def get_account(account_number: str, db: DbSession) -> AccountResponse:
    """Retrieve account information."""

    return AccountResponse.model_validate(AccountService(db).get(account_number))


@router.get("/accounts/{account_number}/balance", response_model=BalanceResponse)
def get_balance(account_number: str, db: DbSession) -> BalanceResponse:
    """Retrieve the current account balance."""

    return AccountService(db).get_balance(account_number)


@router.post(
    "/accounts/{account_number}/transactions",
    response_model=TransactionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_transaction(
    account_number: str, payload: TransactionCreate, db: DbSession
) -> TransactionResponse:
    """Post a credit or debit transaction."""

    return TransactionResponse.model_validate(
        TransactionService(db).create(account_number, payload)
    )


@router.get(
    "/accounts/{account_number}/transactions", response_model=list[TransactionResponse]
)
def list_transactions(
    account_number: str,
    db: DbSession,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> list[TransactionResponse]:
    """Retrieve paginated transaction history."""

    transactions = TransactionService(db).list_for_account(account_number, limit, offset)
    return [TransactionResponse.model_validate(transaction) for transaction in transactions]
