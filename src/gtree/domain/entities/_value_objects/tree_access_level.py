from enum import StrEnum, auto
from functools import total_ordering

from gtree.domain.exceptions import DomainValidationException


@total_ordering
class TreeAccessLevel(StrEnum):
    """Value object representing a tree access level."""

    NOTHING = auto()
    VIEWER = auto()
    EDITOR = auto()
    OWNER = auto()

    @property
    def rank(self) -> int:
        return _RANK_MAP[self]

    @classmethod
    def from_string(cls, value: str | None) -> "TreeAccessLevel":
        """Create TreeAccessLevel from string."""
        try:
            if value is None:
                return cls.NOTHING

            # Normalize the input string
            normalized = value.strip().upper()
            return cls[normalized]
        except (ValueError, KeyError) as e:
            valid_values = [level.value for level in cls]
            raise DomainValidationException(
                f"Invalid access level: '{value}'. Must be one of: {', '.join(valid_values)}"
            ) from e


_RANK_MAP = {
    TreeAccessLevel.NOTHING: 0,
    TreeAccessLevel.VIEWER: 1,
    TreeAccessLevel.EDITOR: 2,
    TreeAccessLevel.OWNER: 3,
}
