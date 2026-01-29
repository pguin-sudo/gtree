from typing import final

from gtree.application.exceptions.base import ApplicationException


@final
class InvalidCredentialsException(ApplicationException):
    """Raised when invalid credentials are provided."""

    def __init__(self, message: str = "Invalid credentials"):
        super().__init__(message, status_code=401)


@final
class InvalidTokenException(ApplicationException):
    """Raised when an invalid token is provided."""

    def __init__(self, message: str, status_code: int = 401):
        super().__init__(message, status_code)


@final
class PermissionDeniedException(ApplicationException):
    """Raised when a user does not have permission to access a resource."""

    def __init__(self, message: str, status_code: int = 401):
        super().__init__(message, status_code)
