from typing import final

from gtree.application.exceptions.base import ApplicationException


@final
class UnknownIndividualForTreeException(ApplicationException):
    """Raised when an individual is unknown for a tree."""

    def __init__(self, message: str = "Unknown individual for tree"):
        super().__init__(message, status_code=403)
