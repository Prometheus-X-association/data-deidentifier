from abc import ABC, abstractmethod

from src.data_deidentifier.domain.types.entities import Entity, EntityType


class AnalyzerPort(ABC):
    """Contract interface for services who detect PII entities in text."""

    @abstractmethod
    def analyze(
        self,
        text: str,
        language: str,
        entity_types: list[EntityType] | None = None,
        min_score: float = 0.5,
    ) -> list[Entity]:
        """Analyze text to detect PII entities.

        Args:
            text: Text to analyze
            language: Language code of the text
            entity_types: Specific entity types to detect (if None, detect all)
            min_score: Minimum confidence score threshold

        Returns:
            List of detected entities

        Raises:
            AnalyzationError: If analysis fails
        """
        raise NotImplementedError
