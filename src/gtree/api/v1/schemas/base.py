from typing import Self

from pydantic.main import BaseModel

from gtree.domain.entities.base import BaseEntity


class BaseSchema(BaseModel):
    """Base schema class for all schemas in the application.

    Note: This schema does NOT perform business validation.
    """

    @classmethod
    def from_entity(cls, entity: BaseEntity) -> Self:
        """Converts an entity to a schema.

        Args:
            entity: The entity to convert.

        Returns:
            The schema.
        """
        return cls(**entity.model_dump())
