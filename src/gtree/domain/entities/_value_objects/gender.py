from enum import StrEnum


class Gender(StrEnum):
    """Value object representing a gender."""

    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
