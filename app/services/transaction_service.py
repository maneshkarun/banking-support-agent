"""Transaction business operations."""

from secrets import token_hex

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.account import Account, AccountStatus
from app.models.transaction import Transaction, TransactionType
from app.schemas.transaction import TransactionCreate
from app.services.exceptions import BusinessRuleError, NotFoundError


class TransactionService:
    """Post transactions and retrieve account transaction history."""

    def __init__(self, session: Session) -> None:
        """Initialize the service with a database session."""

        self.session = session

    def create(self, customer_id: int, account_number: str, payload: TransactionCreate) -> Transaction:
        """Atomically post a credit or debit and update the account balance."""

        account = self.session.scalar(
            select(Account)
            .where(Account.customer_id == customer_id and Account.account_number == account_number)
            .with_for_update()
        )
        if account is None:
            raise NotFoundError("Account not found")
        if account.status is not AccountStatus.ACTIVE:
            raise BusinessRuleError("Transactions are allowed only on active accounts")
        if payload.transaction_type is TransactionType.DEBIT and account.balance < payload.amount:
            raise BusinessRuleError("Insufficient funds")

        if payload.transaction_type is TransactionType.CREDIT:
            account.balance += payload.amount
        else:
            account.balance -= payload.amount

        transaction = Transaction(
            account_id=account.id,
            transaction_type=payload.transaction_type,
            amount=payload.amount,
            description=payload.description,
            reference=f"TXN-{token_hex(10).upper()}",
        )
        self.session.add(transaction)
        self.session.commit()
        self.session.refresh(transaction)
        return transaction

    def list_for_account(self, customer_id: int, account_number: str, limit: int, offset: int) -> list[Transaction]:
        """Return reverse-chronological paginated transaction history."""

        account = self.session.scalar(
            select(Account).where(Account.customer_id == customer_id and Account.account_number == account_number)
        )
        if account is None:
            raise NotFoundError("Account not found")
        statement = (
            select(Transaction)
            .where(Transaction.account_id == account.id)
            .order_by(Transaction.created_at.desc(), Transaction.id.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(self.session.scalars(statement))

