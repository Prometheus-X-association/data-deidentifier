from abc import ABC, abstractmethod

from src.data_deidentifier.domain.types.anonymization_result import AnonymizationResult
from src.data_deidentifier.domain.types.operators import AnonymizationOperator


class AnonymizerContract(ABC):
    """Abstract base class defining the anonymizer interface."""

    @abstractmethod
    def anonymize_text(
        self,
        text: str,
        operator: AnonymizationOperator,
        language: str,
        min_score: float,
        entity_types: list[str] | None = None,
    ) -> AnonymizationResult:
        """Anonymize PII entities in text.

        Args:
            text: Original text containing PII entities
            operator: Anonymization method
            language: Language code of the text
            min_score: Minimum confidence score threshold
            entity_types: Types of entities to detect (None means all supported types)

        Returns:
            An AnonymizationResult containing the anonymized text and metadata

        Raises:
            AnonymizationError: If anonymization fails
        """
        raise NotImplementedError
