"""SQLAlchemy engine, session, and declarative base configuration."""

from collections.abc import Generator, Iterator
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import get_settings


class Base(DeclarativeBase):
    """Base class for all database models."""


settings = get_settings()
connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
engine = create_engine(settings.database_url, connect_args=connect_args, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


@contextmanager
def session_scope() -> Iterator[Session]:
    """Open a database session and guarantee that it is closed after use."""

    with SessionLocal() as session:
        yield session


def get_db() -> Generator[Session, None, None]:
    """Provide a request-scoped database session for FastAPI dependencies."""

    with session_scope() as session:
        yield session
