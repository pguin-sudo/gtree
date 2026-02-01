from enum import StrEnum, auto

from gtree.domain.exceptions import DomainValidationException


class Gender(StrEnum):
    """Value object representing a gender."""

    MALE = auto()
    FEMALE = auto()
    OTHER = auto()

    @classmethod
    def from_string(cls, value: str | None) -> "Gender":
        """Create Gender from string."""
        try:
            if value is None:
                return cls.OTHER
            return cls(value.lower())
        except ValueError as e:
            valid_values = [level.value for level in cls]
            raise DomainValidationException(
                f"Invalid gender: '{value}'. Must be one of: {', '.join(valid_values)}"
            ) from e
