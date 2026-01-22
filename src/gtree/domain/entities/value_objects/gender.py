from dataclasses import dataclass
from typing import ClassVar, final

from gtree.domain.exceptions import InvalidGenderException


@final
@dataclass(frozen=True, slots=True, kw_only=True, order=True)
class Gender:
    """Value object representing a historical era.

    Ensures that the era value is one of the predefined allowed values.
    """

    _allowed_values: ClassVar[set[str]] = {"male", "female", "other"}
    value: str

    def __post_init__(self) -> None:
        """Validates the era value after initialization.

        Raises:
            InvalidGenderException: If the provided gender value is not allowed.
        """
        if self.value not in self._allowed_values:
            raise InvalidGenderException(f"Invalid gender: {self.value}")

    def __str__(self) -> str:
        """Returns the string representation of the gender."""
        return self.value
