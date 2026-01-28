import jwt


class UtilsException(Exception):
    """Raised when an infrastructure error occurs."""

    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class InvalidTokenError(UtilsException, jwt.InvalidTokenError):
    """Raised when an invalid token is provided."""

    def __init__(self, message: str, status_code: int = 401):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)
