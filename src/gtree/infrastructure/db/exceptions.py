class RepositoryException(Exception):
    """Base class for all repository Exceptions."""

    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class NotFoundException(RepositoryException):
    """Exception raised when a resource is not found."""

    def __init__(self, message: str, status_code: int = 404):
        super().__init__(message, status_code)


class ConflictException(RepositoryException):
    """Exception raised when a conflict occurs during a repository operation."""

    def __init__(self, message: str, status_code: int = 401):
        super().__init__(message, status_code)
