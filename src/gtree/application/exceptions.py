from typing import final

# User


class ApplicationException(Exception):
    """Raised when authentication fails."""


@final
class InvalidCredentialsException(ApplicationException):
    """Raised when invalid credentials are provided."""


@final
class UserInactiveException(ApplicationException):
    """Raised when a user is inactive."""


@final
class InvalidTokenException(ApplicationException):
    """Raised when an invalid token is provided."""
