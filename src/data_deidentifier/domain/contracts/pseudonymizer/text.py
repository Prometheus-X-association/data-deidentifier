from abc import ABC, abstractmethod

from src.data_deidentifier.domain.contracts.enricher import EntityEnricherContract
from src.data_deidentifier.domain.contracts.pseudonymizer.method import (
    PseudonymizationMethodContract,
)
from src.data_deidentifier.domain.types.text_pseudonymization_result import (
    TextPseudonymizationResult,
)


class TextPseudonymizerContract(ABC):
    """Abstract base class defining the text pseudonymizer interface."""

    @abstractmethod
    def pseudonymize(  # noqa: PLR0913
        self,
        text: str,
        method: PseudonymizationMethodContract,
        language: str,
        min_score: float,
        entity_types: list[str] | None = None,
        entity_enricher: EntityEnricherContract | None = None,
    ) -> TextPseudonymizationResult:
        """Pseudonymize PII entities in text.

        Args:
            text: Original text containing PII entities
            method: Pseudonymization method instance
            language: Language code of the text
            min_score: Minimum confidence score threshold
            entity_types: Types of entities to detect (None means all supported types)
            entity_enricher: Optional enrichment service for adding contextual
                information to pseudonyms found in structured data

        Returns:
            A TextPseudonymizationResult containing the pseudonymized text and metadata

        Raises:
            TextPseudonymizationError: If pseudonymization fails
        """
        raise NotImplementedError
