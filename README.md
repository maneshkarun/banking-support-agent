# Simple Banking API

A small FastAPI application for customer registration, account information, balance checks,
credits/debits, and transaction history. It uses FastAPI, Pydantic v2, SQLAlchemy 2, and SQLite.

## Run locally

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` for interactive OpenAPI documentation.

## API endpoints

- `POST /api/v1/customers`
- `GET /api/v1/customers/{customer_id}`
- `POST /api/v1/accounts`
- `GET /api/v1/accounts/{account_number}`
- `GET /api/v1/accounts/{account_number}/balance`
- `POST /api/v1/accounts/{account_number}/transactions`
- `GET /api/v1/accounts/{account_number}/transactions?limit=20&offset=0`
- `GET /health`

## Quality checks

```powershell
pytest
ruff check .
```

SQLite tables are created automatically at startup. For larger deployments, replace this with
Alembic migrations and use PostgreSQL; set `DATABASE_URL` in `.env` (see `.env.example`).
