from dataclasses import dataclass


@dataclass
class Entity:
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
    """

    type: str
    start: int
    end: int
    score: float
    text: str | None = None
