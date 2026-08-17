"""Shared API test fixtures."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.main import app


@pytest.fixture
def client() -> TestClient:
    """Provide an isolated in-memory API client."""

    test_engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    test_session = sessionmaker(bind=test_engine, expire_on_commit=False)
    Base.metadata.create_all(test_engine)

    def override_db() -> Session:
        with test_session() as session:
            yield session

    app.dependency_overrides[get_db] = override_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    Base.metadata.drop_all(test_engine)

