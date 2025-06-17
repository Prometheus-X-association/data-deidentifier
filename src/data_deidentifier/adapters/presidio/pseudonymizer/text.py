from typing import Any, override

from logger import LoggerContract

from src.data_deidentifier.adapters.presidio.anonymizer.text import (
    PresidioTextAnonymizer,
)
from src.data_deidentifier.domain.contracts.pseudonymizer.text import (
    TextPseudonymizerContract,
)
from src.data_deidentifier.domain.exceptions import (
    TextAnonymizationError,
    TextPseudonymizationError,
)
from src.data_deidentifier.domain.services.pseudonymization.methods.factory import (
    PseudonymizationMethodFactory,
)
from src.data_deidentifier.domain.types.anonymization_operator import (
    AnonymizationOperator,
)
from src.data_deidentifier.domain.types.pseudonymization_method import (
    PseudonymizationMethod,
)
from src.data_deidentifier.domain.types.text_pseudonymization_result import (
    TextPseudonymizationResult,
)

from .custom_operator import PseudonymizeOperator


class PresidioTextPseudonymizer(TextPseudonymizerContract):
    """Implementation of pseudonymizer contract using Microsoft Presidio."""

    def __init__(self, logger: LoggerContract) -> None:
        """Initialize the Presidio text pseudonymizer.

        Args:
            logger: Logger for logging events
        """
        self.logger = logger

        self.anonymizer = PresidioTextAnonymizer(logger=self.logger)

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
        logger_context = {
            "text_length": len(text),
            "method": method.value,
        }
        self.logger.debug("Starting text pseudonymization", logger_context)

        # Get the pseudonymization method
        pseudonymization_method = PseudonymizationMethodFactory.create(
            method=method,
            params=method_params,
        )

        # Delegate to anonymizer with our custom operator
        try:
            anonymization_result = self.anonymizer.anonymize(
                text=text,
                operator=AnonymizationOperator.PSEUDONYMIZE,
                language=language,
                min_score=min_score,
                entity_types=entity_types,
                operator_params={
                    PseudonymizeOperator.PARAM_METHOD: pseudonymization_method,
                },
            )
        except TextAnonymizationError as e:
            raise TextPseudonymizationError(
                "Pseudonymization failed during anonymization",
            ) from e

        self.logger.info("Text pseudonymization completed successfully", logger_context)

        # Adapt the result
        return TextPseudonymizationResult(
            pseudonymized_text=anonymization_result.anonymized_text,
            detected_entities=anonymization_result.detected_entities,
        )
