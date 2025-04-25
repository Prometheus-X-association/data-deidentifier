from dataclasses import dataclass

from .entity import Entity


@dataclass
class AnalysisResult:
    """Result of a text analysis operation.

    This class encapsulates all information about an analysis operation,
    including detected entities and analysis metadata.

    Attributes:
        entities: List of detected entities in the text
        language: Language code used for the analysis
        min_score: Minimum confidence score used for detection
        entity_stats: Statistics of detected entity types and their counts
    """

    entities: list[Entity]
    language: str
    min_score: float
    entity_stats: dict[str, int] | None = None
