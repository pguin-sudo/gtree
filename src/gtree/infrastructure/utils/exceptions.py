import jwt


class UtilsException(Exception):
    """Raised when an infrastructure error occurs."""


class InvalidTokenError(UtilsException, jwt.InvalidTokenError):
    """Raised when an invalid token is provided."""
