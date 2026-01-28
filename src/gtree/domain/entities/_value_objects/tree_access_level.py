from enum import StrEnum


class TreeAccessLevel(StrEnum):
    """Value object representing a tree access level."""

    NOTHING = "nothing"
    VIEWER = "viewer"
    EDITOR = "editor"
    OWNER = "owner"

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
