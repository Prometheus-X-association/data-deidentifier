from typing import Any, override

from logger import LoggerContract

from src.data_deidentifier.domain.contracts.pseudonymizer.text import (
    TextPseudonymizerContract,
)
from src.data_deidentifier.domain.types.pseudonymization_method import (
    PseudonymizationMethod,
)
from src.data_deidentifier.domain.types.text_pseudonymization_result import (
    TextPseudonymizationResult,
)


class PresidioTextPseudonymizer(TextPseudonymizerContract):
    """Implementation of pseudonymizer contract using Microsoft Presidio."""

    def __init__(self, logger: LoggerContract) -> None:
        """Initialize the Presidio text pseudonymizer.

        Args:
            logger: Logger for logging events
        """
        self.logger = logger

        self.logger.debug("Presidio Pseudonymizer initialized successfully")

    @override
    def pseudonymize(
        self,
        text: str,
        method: PseudonymizationMethod,
        language: str,
        min_score: float,
        entity_types: list[str] | None = None,
        method_params: dict[str, Any] | None = None,
    ) -> TextPseudonymizationResult:
        return TextPseudonymizationResult(pseudonymized_text=text, detected_entities=[])
