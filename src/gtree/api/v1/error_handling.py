from fastapi import Request, status
from fastapi.applications import FastAPI
from fastapi.responses import JSONResponse

from gtree.application import exceptions as application_exceptions
from gtree.domain import exceptions as domain_exceptions
from gtree.infrastructure.db import exceptions as db_exceptions
from gtree.infrastructure.utils import exceptions as utils_exceptions

ERROR_MAPPING = {
    # DOMAIN
    domain_exceptions.InvalidGenderException: status.HTTP_400_BAD_REQUEST,
    # APPLICATION
    application_exceptions.ApplicationException: status.HTTP_400_BAD_REQUEST,
    # INFRASTRUCTURES
    utils_exceptions.UtilsException: status.HTTP_400_BAD_REQUEST,
    db_exceptions.RepositoryException: status.HTTP_400_BAD_REQUEST,
}


def setup_exception_handlers(app: FastAPI):
    """Setup exception handlers for the application."""

    @app.exception_handler(domain_exceptions.DomainException)
    def domain_exception_handler(
        _: Request, exc: domain_exceptions.DomainException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=ERROR_MAPPING.get(exc, status.HTTP_400_BAD_REQUEST),
            content={"message": str(exc)},
        )

    @app.exception_handler(application_exceptions.ApplicationException)
    def application_exception_handler(
        _: Request, exc: application_exceptions.ApplicationException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=ERROR_MAPPING.get(exc, status.HTTP_400_BAD_REQUEST),
            content={"message": str(exc)},
        )

    @app.exception_handler(utils_exceptions.UtilsException)
    def utils_exception_handler(
        _: Request, exc: utils_exceptions.UtilsException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=ERROR_MAPPING.get(exc, status.HTTP_400_BAD_REQUEST),
            content={"message": str(exc)},
        )

    @app.exception_handler(db_exceptions.RepositoryException)
    def db_exception_handler(
        _: Request, exc: db_exceptions.RepositoryException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=ERROR_MAPPING.get(exc, status.HTTP_400_BAD_REQUEST),
            content={"message": str(exc)},
        )
