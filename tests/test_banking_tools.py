"""Regression tests for database sessions used by LangChain tools."""

from decimal import Decimal

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core import database
from app.core.database import Base
from app.models.account import Account, AccountType
from app.models.customer import Customer
from app.tools.banking_tools import (
    get_account_balance,
    get_complete_account_details,
    get_customer_details,
)


@pytest.fixture
def tool_database(monkeypatch: pytest.MonkeyPatch) -> None:
    """Point direct tool sessions at an isolated in-memory database."""

    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    session_factory = sessionmaker(bind=engine, expire_on_commit=False)
    Base.metadata.create_all(engine)
    monkeypatch.setattr(database, "SessionLocal", session_factory)

    with session_factory() as session:
        customer = Customer(full_name="Asha Rao", email="asha@example.com")
        session.add(customer)
        session.flush()
        session.add(
            Account(
                account_number="AC123456",
                customer_id=customer.id,
                account_type=AccountType.SAVINGS,
                balance=Decimal("725.50"),
            )
        )
        session.commit()

    yield
    Base.metadata.drop_all(engine)


def test_tools_resolve_real_sessions_and_return_serializable_data(tool_database: None) -> None:
    """Each tool call uses a real session and returns JSON-safe values."""

    customer = get_customer_details.invoke({"customer_id": 1})
    account = get_complete_account_details.invoke({"account_number": "AC123456"})
    balance = get_account_balance.invoke({"account_number": "AC123456"})

    assert customer["email"] == "asha@example.com"
    assert account["account_type"] == "savings"
    assert balance == {
        "account_number": "AC123456",
        "currency": "INR",
        "balance": "725.50",
    }
