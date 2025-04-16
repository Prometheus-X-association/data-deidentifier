from pydantic import BaseModel

from src.data_deidentifier.domain.utils.utils_enum import UpperStrEnum


class EntityType(UpperStrEnum):
    """Base enum for entity types recognized by the system.

    This enum is intentionally empty to allow inheritance by specific implementations.
    Subclasses should define their own entity types by adding enum members.

    !!! LEAVE IT EMPTY TO AVOID TypeError !!!
    """


class Entity(BaseModel):
    """Represents a detected PII entity in content.

    This model captures information about a personally identifiable information (PII)
    entity detected in text or JSON content
    including its type, position, and confidence score.

    Attributes:
        type: The type of PII entity detected
        start: The starting position of the entity in the content
        end: The ending position of the entity in the content
        score: The confidence score of the detection (0.0 to 1.0)
        text: The actual text of the detected entity
        path: For JSON data, the dot notation path to the field containing the entity
    """

    type: EntityType
    start: int
    end: int
    score: float
    text: str | None = None
    path: str | None = None  # For JSON data, dot notation path to the field
