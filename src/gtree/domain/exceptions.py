from typing import final


class DomainException(Exception):
    """Raised when a domain error occurs."""


@final
class InvalidGenderException(DomainException):
    """Raised when an invalid gender is provided."""
