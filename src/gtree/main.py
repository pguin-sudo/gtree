from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import structlog

from gtree.api.v1.error_handling import setup_exception_handlers
from gtree.api.v1.routers import api_v1_router
from gtree.core.logging import setup_logging

setup_logging()
logger = structlog.get_logger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """Asynchronous context manager for managing the lifespan of the FastAPI application.

    Args:
        _: The FastAPI application instance.

    Yields:
        None
    """
    logger.info("Starting application...")
    yield
    logger.info("Shutting down application...")


def create_app() -> FastAPI:
    """Creates and configures the FastAPI application.

    Returns:
        FastAPI: The configured FastAPI application instance.
    """
    app = FastAPI(
        title="GTree API",
        version="1.0.0",
        description="API for A modern FastAPI application with clean architecture",
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    app.add_middleware(  # type: ignore[call-arg]
        CORSMiddleware,  # type: ignore[arg-type]
        allow_origins=[
            "http://localhost",
            "http://localhost:8080",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    setup_exception_handlers(app)
    app.include_router(api_v1_router, prefix="/api/v1")

    return app


app = create_app()
