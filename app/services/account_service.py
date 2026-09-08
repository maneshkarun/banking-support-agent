"""Account business operations."""

from secrets import token_hex

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.account import Account
from app.models.customer import Customer
from app.schemas.account import AccountCreate, BalanceResponse, AccountResponse
from app.services.exceptions import NotFoundError

from typing import List

class AccountService:
    """Provide account opening, information, and balance operations."""

    def __init__(self, session: Session) -> None:
        """Initialize the service with a database session."""

        self.session = session

    def create(self, customer_id: int, payload: AccountCreate) -> Account:
        """Open an account for an existing customer with a unique number."""

        if self.session.get(Customer, customer_id) is None:
            raise NotFoundError("Customer not found")
        account = Account(
            account_number=f"AC{token_hex(8).upper()}",
            customer_id=payload.customer_id,
            account_type=payload.account_type,
            currency=payload.currency,
            balance=payload.opening_balance,
        )
        self.session.add(account)
        self.session.commit()
        self.session.refresh(account)
        return account

    def get(self, customer_id: int | str, account_number: str | None = None) -> Account:
        """Return account information by account number."""

        if account_number is None:
            account = self.session.scalar(
                select(Account).where(Account.account_number == customer_id)
            )
        else:
            account = self.session.scalar(
                select(Account).where(
                    Account.account_number == account_number,
                    Account.customer_id == customer_id,
                )
            )
        if account is None:
            raise NotFoundError("Account not found")
        return account
    
    def get_customer_account(self, customer_id: int) -> List[AccountResponse]:
        accounts = self.session.scalars(
            select(Account).where(Account.customer_id == customer_id)
        ).all()
        return [
            AccountResponse.model_validate(account) for account in accounts
        ]
    
    def get_balance(
        self, customer_id: int | str, account_number: str | None = None
    ) -> BalanceResponse:
        """Return the current ledger balance for an account."""

        account = self.get(customer_id, account_number)
        return BalanceResponse(
            account_number=account.account_number,
            currency=account.currency,
            balance=account.balance,
        )
