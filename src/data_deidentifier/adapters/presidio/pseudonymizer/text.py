from typing import override

from logger import LoggerContract

from src.data_deidentifier.adapters.infrastructure.config.contract import ConfigContract
from src.data_deidentifier.adapters.presidio.anonymizer.text import (
    PresidioTextAnonymizer,
)
from src.data_deidentifier.domain.contracts.enricher import EntityEnricherContract
from src.data_deidentifier.domain.contracts.pseudonymizer.method import (
    PseudonymizationMethodContract,
)
from src.data_deidentifier.domain.contracts.pseudonymizer.text import (
    TextPseudonymizerContract,
)
from src.data_deidentifier.domain.exceptions import (
    TextAnonymizationError,
    TextPseudonymizationError,
)
from src.data_deidentifier.domain.types.anonymization_operator import (
    AnonymizationOperator,
)
from src.data_deidentifier.domain.types.text_pseudonymization_result import (
    TextPseudonymizationResult,
)

from .custom_operator import PseudonymizeOperator


class PresidioTextPseudonymizer(TextPseudonymizerContract):
    """Implementation of text pseudonymizer contract using Microsoft Presidio."""

    def __init__(self, config: ConfigContract, logger: LoggerContract) -> None:
        """Initialize the Presidio text pseudonymizer.

        Args:
            config: Configuration contract.
            logger: Logger for logging events
        """
        self.config = config
        self.logger = logger

        self.anonymizer = PresidioTextAnonymizer(logger=self.logger)

        self.logger.debug("Presidio text Pseudonymizer initialized successfully")

    @override
    def pseudonymize(
        self,
        text: str,
        method: PseudonymizationMethodContract,
        language: str,
        min_score: float,
        entity_types: list[str] | None = None,
        entity_enricher: EntityEnricherContract | None = None,
    ) -> TextPseudonymizationResult:
        logger_context = {
            "method": type(method).__name__,
        }
        self.logger.debug("Starting text pseudonymization", logger_context)

        operator_params = {
            PseudonymizeOperator.PARAM_METHOD: method,
        }

        if entity_enricher:
            url_mappings = self.config.get_enrichment_url_mappings()
            enrichable_types = set(url_mappings.keys())
            if enrichable_types:
                operator_params.update(
                    {
                        PseudonymizeOperator.PARAM_ENRICHER: entity_enricher,
                        PseudonymizeOperator.PARAM_ENRICHABLE_TYPES: enrichable_types,
                    },
                )

        # Delegate to anonymizer with our custom operator
        try:
            anonymization_result = self.anonymizer.anonymize(
                text=text,
                operator=AnonymizationOperator.PSEUDONYMIZE,
                language=language,
                min_score=min_score,
                entity_types=entity_types,
                operator_params=operator_params,
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
