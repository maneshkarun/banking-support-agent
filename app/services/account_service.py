"""Account business operations."""

from secrets import token_hex

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.account import Account
from app.models.customer import Customer
from app.schemas.account import AccountCreate, BalanceResponse
from app.services.exceptions import NotFoundError


class AccountService:
    """Provide account opening, information, and balance operations."""

    def __init__(self, session: Session) -> None:
        """Initialize the service with a database session."""

        self.session = session

    def create(self, payload: AccountCreate) -> Account:
        """Open an account for an existing customer with a unique number."""

        if self.session.get(Customer, payload.customer_id) is None:
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

    def get(self, account_number: str) -> Account:
        """Return account information by account number."""

        account = self.session.scalar(
            select(Account).where(Account.account_number == account_number)
        )
        if account is None:
            raise NotFoundError("Account not found")
        return account

    def get_balance(self, account_number: str) -> BalanceResponse:
        """Return the current ledger balance for an account."""

        account = self.get(account_number)
        return BalanceResponse(
            account_number=account.account_number,
            currency=account.currency,
            balance=account.balance,
        )