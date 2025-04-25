from abc import ABC, abstractmethod

from src.data_deidentifier.domain.types.entity import Entity


class AnalyzerContract(ABC):
    """Abstract base class defining the analyzer interface."""

    @abstractmethod
    def analyze_text(
        self,
        text: str,
        language: str,
        min_score: float,
    ) -> list[Entity]:
        """Analyze text to detect PII entities.

        Args:
            text: Text to analyze
            language: Language code of the text
            min_score: Minimum confidence score threshold

        Returns:
            List of detected entities

        Raises:
            AnalyzationError: If analysis fails
        """
        raise NotImplementedError
