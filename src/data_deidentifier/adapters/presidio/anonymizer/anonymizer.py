from typing import override

from logger import LoggerContract
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

from src.data_deidentifier.adapters.presidio.analyzer.analyzer import PresidioAnalyzer
from src.data_deidentifier.adapters.presidio.mapper import PresidioEntityMapper
from src.data_deidentifier.domain.contracts.anonymizer import AnonymizerContract
from src.data_deidentifier.domain.exceptions import AnonymizationError
from src.data_deidentifier.domain.types.anonymization_operator import (
    AnonymizationOperator,
)
from src.data_deidentifier.domain.types.anonymization_result import AnonymizationResult


class PresidioAnonymizer(AnonymizerContract):
    """Implementation of anonymizer contract using Microsoft Presidio."""

    def __init__(self, logger: LoggerContract) -> None:
        """Initialize the Presidio anonymizer.

        Args:
            logger: Logger for logging events
        """
        self.logger = logger

        self.presidio_anonymizer = AnonymizerEngine()
        self.analyzer = PresidioAnalyzer(logger=self.logger)

        self.logger.debug("Presidio Anonymizer initialized successfully")

    @override
    def anonymize_text(
        self,
        text: str,
        operator: AnonymizationOperator,
        language: str,
        min_score: float,
        entity_types: list[str] | None = None,
    ) -> AnonymizationResult:
        # Analyze to detect PII entities in text
        analyzer_results = self.analyzer.analyze_text(
            text=text,
            language=language,
            min_score=min_score,
            entity_types=entity_types,
        )

        if not text or not analyzer_results:
            return AnonymizationResult(
                anonymized_text=text,
                detected_entities=[],
            )

        logger_context = {
            "text_length": len(text),
            "entities_count": len(analyzer_results),
            "operator": operator.value,
        }
        self.logger.debug("Starting text anonymization", logger_context)

        # Prepare operator config
        entity_types = {entity.entity_type for entity in analyzer_results}
        operator_config = OperatorConfig(operator_name=operator)
        operators = {entity_type: operator_config for entity_type in entity_types}

        try:
            # Anonymize the text
            presidio_results = self.presidio_anonymizer.anonymize(
                text=text,
                analyzer_results=analyzer_results,
                operators=operators,
            )
        except Exception as e:
            msg = "Unexpected error during text anonymization"
            self.logger.exception(msg, e, logger_context)
            raise AnonymizationError(msg) from e

        self.logger.info("Text anonymization completed successfully", logger_context)

        # Convert results to our format
        entities = [
            PresidioEntityMapper.presidio_result_to_entity(
                result=result,
                text=text,
            )
            for result in analyzer_results
        ]

        return AnonymizationResult(
            anonymized_text=presidio_results.text,
            detected_entities=entities,
        )
