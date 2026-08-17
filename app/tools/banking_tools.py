"""LangChain tools that expose read-only banking operations."""

from typing import Any

from langchain.tools import tool

from app.core.database import session_scope
from app.schemas.account import AccountResponse
from app.schemas.customer import CustomerResponse
from app.services.account_service import AccountService
from app.services.customer_service import CustomerService


def _json_result(value: CustomerResponse | AccountResponse) -> dict[str, Any]:
    """Convert a response DTO to values that an agent can safely serialize."""

    return value.model_dump(mode="json")


@tool
def get_customer_details(customer_id: int) -> dict[str, Any]:
    """Fetch customer details using a positive customer identifier."""

    with session_scope() as session:
        customer = CustomerService(session).get(customer_id)
        return _json_result(CustomerResponse.model_validate(customer))


@tool
def get_account_balance(account_number: str) -> dict[str, Any]:
    """Fetch the current balance and currency using an account number."""

    with session_scope() as session:
        balance = AccountService(session).get_balance(account_number)
        return balance.model_dump(mode="json")


@tool
def get_complete_account_details(account_number: str) -> dict[str, Any]:
    """Fetch complete account details using an account number."""

    with session_scope() as session:
        account = AccountService(session).get(account_number)
        return _json_result(AccountResponse.model_validate(account))
