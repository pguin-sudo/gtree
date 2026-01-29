from pydantic.main import BaseModel


class BaseSchema(BaseModel):
    """Base schema class for all schemas in the application.

    Note: This schema does NOT perform business validation.
    """
