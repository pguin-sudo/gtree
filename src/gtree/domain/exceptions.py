class DomainException(Exception):
    """Raised when a domain error occurs."""

    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class DomainValidationException(DomainException):
    """Raised when a domain validation error occurs."""

    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message, status_code)
