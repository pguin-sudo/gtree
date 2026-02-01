from typing import final

from gtree.application.exceptions.base import ApplicationException


@final
class UserInactiveException(ApplicationException):
    """Raised when a user is inactive."""

    def __init__(self, message: str = "User is inactive"):
        super().__init__(message, status_code=403)
