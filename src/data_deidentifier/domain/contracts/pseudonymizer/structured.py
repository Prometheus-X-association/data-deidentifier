from abc import ABC, abstractmethod
from typing import Any

from src.data_deidentifier.domain.types.pseudonymization_method import (
    PseudonymizationMethod,
)
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
        method: PseudonymizationMethod,
        language: str,
        entity_types: list[str] | None = None,
        method_params: dict[str, Any] | None = None,
    ) -> StructuredDataPseudonymizationResult:
        """Pseudonymize PII entities in structured data.

        Args:
            data: Original structured data containing PII entities
            method: Pseudonymization method
            language: Language code of the data
            entity_types: Types of entities to detect (None means all supported types)
            method_params: Optional parameters for the method

        Returns:
            A StructuredDataPseudonymizationResult
            containing the pseudonymized data and metadata

        Raises:
            StructuredDataPseudonymizationError: If pseudonymization fails
        """
        raise NotImplementedError
