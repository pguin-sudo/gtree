import logging

from fastapi import Request, status
from fastapi.applications import FastAPI
from fastapi.responses import JSONResponse

from gtree.application.exceptions import base as application_exceptions
from gtree.domain import exceptions as domain_exceptions
from gtree.infrastructure.db import exceptions as db_exceptions
from gtree.infrastructure.utils import exceptions as utils_exceptions

logger = logging.getLogger(__name__)


def setup_exception_handlers(app: FastAPI):
    """Setup exception handlers for the application."""

    @app.exception_handler(domain_exceptions.DomainException)
    def domain_exception_handler(
        _: Request, exc: domain_exceptions.DomainException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"message": str(exc.message)},
        )

    @app.exception_handler(application_exceptions.ApplicationException)
    def application_exception_handler(
        _: Request, exc: application_exceptions.ApplicationException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"message": str(exc.message)},
        )

    @app.exception_handler(utils_exceptions.UtilsException)
    def utils_exception_handler(
        _: Request, exc: utils_exceptions.UtilsException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"message": str(exc.message)},
        )

    @app.exception_handler(db_exceptions.RepositoryException)
    def db_exception_handler(
        _: Request, exc: db_exceptions.RepositoryException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"message": str(exc.message)},
        )

    @app.exception_handler(Exception)
    def other_exception_handler(_: Request, exc: Exception) -> JSONResponse:
        logger.error("Unhandled exception: {%s}", exc)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "GTree Internal Server Error"},
        )
