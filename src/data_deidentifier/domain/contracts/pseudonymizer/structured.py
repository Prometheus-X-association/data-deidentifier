from abc import ABC, abstractmethod

from src.data_deidentifier.domain.contracts.enricher.manager import (
    PseudonymEnrichmentManagerContract,
)
from src.data_deidentifier.domain.contracts.pseudonymizer.method import (
    PseudonymizationMethodContract,
)
from src.data_deidentifier.domain.types.language import SupportedLanguage
from src.data_deidentifier.domain.types.structured_data import StructuredData
from src.data_deidentifier.domain.types.structured_pseudonymization_result import (
    StructuredDataPseudonymizationResult,
)


class StructuredDataPseudonymizerContract(ABC):
    """Abstract base class defining the structured data pseudonymizer interface."""

    @abstractmethod
    def pseudonymize(
        self,
        data: StructuredData,
        method: PseudonymizationMethodContract,
        language: SupportedLanguage,
        entity_types: list[str] | None = None,
        pseudonym_enricher: PseudonymEnrichmentManagerContract | None = None,
    ) -> StructuredDataPseudonymizationResult:
        """Pseudonymize PII entities in structured data.

        Args:
            data: Original structured data containing PII entities
            method: Pseudonymization method instance
            language: Language code of the data
            entity_types: Types of entities to detect (None means all supported types)
            pseudonym_enricher: Optional enrichment service for adding contextual
                information to pseudonyms found in structured data

        Returns:
            A StructuredDataPseudonymizationResult
            containing the pseudonymized data and metadata

        Raises:
            StructuredDataPseudonymizationError: If pseudonymization fails
        """
        raise NotImplementedError
