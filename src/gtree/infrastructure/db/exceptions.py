class RepositoryException(Exception):
    """Base class for all repository Exceptions."""


class NotFoundException(RepositoryException):
    """Exception raised when a resource is not found."""


class DuplicateException(RepositoryException):
    """Exception raised when a duplicate resource is found."""


class AlreadyExistsException(RepositoryException):
    """Exception raised when a resource already exists."""


class ConflictException(RepositoryException):
    """Exception raised when a conflict occurs during a repository operation."""


class SaveException(RepositoryException):
    """Exception raised when a resource fails to save."""
