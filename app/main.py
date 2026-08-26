"""FastAPI application entry point."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app import models  # noqa: F401
from app.api.routes import router
from app.core.config import get_settings
from app.core.database import Base, engine
from app.services.exceptions import BusinessRuleError, ConflictError, NotFoundError
from app.agents.agent import build_agent

from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Create database tables on startup for this lightweight application."""

    Base.metadata.create_all(bind=engine)
    app.state.banking_agent = build_agent()

    yield


settings = get_settings()
app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    debug=settings.debug,
    lifespan=lifespan,
)
app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", tags=["operations"])
def health() -> dict[str, str]:
    """Return the API health status."""

    return {"status": "ok"}


@app.exception_handler(NotFoundError)
async def not_found_handler(_: Request, exc: NotFoundError) -> JSONResponse:
    """Translate missing domain resources into HTTP 404 responses."""

    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": str(exc)})


@app.exception_handler(ConflictError)
async def conflict_handler(_: Request, exc: ConflictError) -> JSONResponse:
    """Translate state conflicts into HTTP 409 responses."""

    return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"detail": str(exc)})


@app.exception_handler(BusinessRuleError)
async def business_rule_handler(_: Request, exc: BusinessRuleError) -> JSONResponse:
    """Translate invalid business operations into HTTP 422 responses."""

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={"detail": str(exc)}
    )
