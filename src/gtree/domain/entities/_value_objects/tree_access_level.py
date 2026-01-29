from enum import StrEnum, auto

from gtree.domain.exceptions import DomainValidationException


class TreeAccessLevel(StrEnum):
    """Value object representing a tree access level."""

    NOTHING = auto()
    VIEWER = auto()
    EDITOR = auto()
    OWNER = auto()

    @property
    def rank(self) -> int:
        return {
            self.NOTHING: 0,
            self.VIEWER: 1,
            self.EDITOR: 2,
            self.OWNER: 3,
        }[self]

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, TreeAccessLevel):
            return NotImplemented
        return self.rank < other.rank

    @classmethod
    def from_string(cls, value: str) -> "TreeAccessLevel":
        """Create TreeAccessLevel from string."""
        try:
            return cls(value.lower())
        except ValueError as e:
            valid_values = [level.value for level in cls]
            raise DomainValidationException(
                f"Invalid access level: '{value}'. Must be one of: {', '.join(valid_values)}"
            ) from e
