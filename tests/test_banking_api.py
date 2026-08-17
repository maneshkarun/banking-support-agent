"""End-to-end tests for core banking operations."""

from fastapi.testclient import TestClient


def open_account(client: TestClient, opening_balance: str = "1000.00") -> str:
    """Create a customer and return a newly opened account number."""

    customer = client.post(
        "/api/v1/customers",
        json={"full_name": "Asha Rao", "email": "asha@example.com"},
    ).json()
    response = client.post(
        "/api/v1/accounts",
        json={
            "customer_id": customer["id"],
            "account_type": "savings",
            "opening_balance": opening_balance,
        },
    )
    assert response.status_code == 201
    return response.json()["account_number"]


def test_balance_and_transaction_history(client: TestClient) -> None:
    """Credits and debits update balance and appear in transaction history."""

    account_number = open_account(client)
    credit = client.post(
        f"/api/v1/accounts/{account_number}/transactions",
        json={"transaction_type": "credit", "amount": "250.50", "description": "Salary"},
    )
    debit = client.post(
        f"/api/v1/accounts/{account_number}/transactions",
        json={"transaction_type": "debit", "amount": "100.25", "description": "Groceries"},
    )

    assert credit.status_code == 201
    assert debit.status_code == 201
    assert client.get(f"/api/v1/accounts/{account_number}/balance").json()["balance"] == "1150.25"
    history = client.get(f"/api/v1/accounts/{account_number}/transactions").json()
    assert [item["description"] for item in history] == ["Groceries", "Salary"]


def test_rejects_overdraft(client: TestClient) -> None:
    """A debit greater than the available balance is rejected."""

    account_number = open_account(client, "50.00")
    response = client.post(
        f"/api/v1/accounts/{account_number}/transactions",
        json={"transaction_type": "debit", "amount": "50.01"},
    )
    assert response.status_code == 422
    assert response.json() == {"detail": "Insufficient funds"}


def test_duplicate_customer_email_is_rejected(client: TestClient) -> None:
    """Customer emails remain unique."""

    payload = {"full_name": "Asha Rao", "email": "asha@example.com"}
    assert client.post("/api/v1/customers", json=payload).status_code == 201
    assert client.post("/api/v1/customers", json=payload).status_code == 409

