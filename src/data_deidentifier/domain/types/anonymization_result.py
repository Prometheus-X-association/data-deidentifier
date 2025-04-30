from dataclasses import dataclass


@dataclass
class AnonymizationResult:
    """Result of a text anonymization operation.

    This class encapsulates all information about an anonymization operation,
    including the anonymized text and metadata.

    Attributes:
        anonymized_text: The text after anonymization
        operator: The anonymization operator used
        entity_stats: Statistics of anonymized entity types and their counts
    """

    anonymized_text: str
    operator: str
    entity_stats: dict[str, int] | None = None
