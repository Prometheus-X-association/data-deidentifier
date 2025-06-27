from dataclasses import dataclass

from .entity import Entity


@dataclass
class TextAnonymizationResult:
    """Result of a text anonymization operation.

    This class encapsulates all information about an anonymization operation.

    Attributes:
        anonymized_text: The text after anonymization
        detected_entities: List of PII entities that were detected and anonymized
    """

    anonymized_text: str
    detected_entities: list[Entity]
