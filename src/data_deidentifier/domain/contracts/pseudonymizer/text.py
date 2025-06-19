from abc import ABC, abstractmethod
from typing import Any

from src.data_deidentifier.domain.types.pseudonymization_method import (
    PseudonymizationMethod,
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
        method: PseudonymizationMethod,
        language: str,
        min_score: float,
        entity_types: list[str] | None = None,
        method_params: dict[str, Any] | None = None,
    ) -> TextPseudonymizationResult:
        """Pseudonymize PII entities in text.

        Args:
            text: Original text containing PII entities
            method: Pseudonymization method
            language: Language code of the text
            min_score: Minimum confidence score threshold
            entity_types: Types of entities to detect (None means all supported types)
            method_params: Optional parameters for the method

        Returns:
            A TextPseudonymizationResult containing the pseudonymized text and metadata

        Raises:
            TextPseudonymizationError: If pseudonymization fails
        """
        raise NotImplementedError
