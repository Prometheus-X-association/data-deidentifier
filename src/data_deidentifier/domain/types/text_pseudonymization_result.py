from dataclasses import dataclass

from .entity import Entity


@dataclass
class TextPseudonymizationResult:
    """Result of a text pseudonymization operation.

    This class encapsulates all information about a pseudonymization operation.

    Attributes:
        pseudonymized_text: The text after pseudonymization
        detected_entities: List of PII entities that were detected and pseudonymized
    """

    pseudonymized_text: str
    detected_entities: list[Entity]
