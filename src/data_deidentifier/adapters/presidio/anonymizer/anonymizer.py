from typing import override

from logger import LoggerContract
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig, RecognizerResult

from src.data_deidentifier.domain.exceptions import AnonymizationError
from src.data_deidentifier.domain.types.entities import Entity
from src.data_deidentifier.domain.types.operators import AnonymizationOperator
from src.data_deidentifier.ports.anonymizer_port import AnonymizerPort


class PresidioAnonymizer(AnonymizerPort):
    """Implementation of anonymizer port using Microsoft Presidio."""

    def __init__(self, logger: LoggerContract) -> None:
        """Initialize the Presidio anonymizer.

        Args:
            logger: Logger for logging events
        """
        self.logger = logger

        self.anonymizer = AnonymizerEngine()

        self.logger.debug("Presidio Anonymizer initialized successfully")

    @override
    def anonymize_text(
        self,
        text: str,
        entities: list[Entity],
        operator: AnonymizationOperator,
    ) -> str:
        if not text or not entities:
            return text

        logger_context = {
            "text_length": len(text),
            "entities_count": len(entities),
            "operator": operator.value,
        }
        self.logger.debug("Starting text anonymization", logger_context)

        # Convert our entities to Presidio's RecognizerResult format
        analyzer_results = self._convert_entities_to_presidio_format(entities)

        # Prepare operator config
        entity_types = {entity.type for entity in entities}
        operator_config = OperatorConfig(operator_name=operator)
        operators = {entity_type: operator_config for entity_type in entity_types}

        try:
            # Anonymize the text
            result = self.anonymizer.anonymize(
                text=text,
                analyzer_results=analyzer_results,
                operators=operators,
            )
        except Exception as e:
            msg = "Unexpected error during text anonymization"
            self.logger.exception(msg, e, logger_context)
            raise AnonymizationError(msg) from e

        self.logger.info("Text anonymization completed successfully", logger_context)

        return result.text

    def _convert_entities_to_presidio_format(
        self,
        entities: list[Entity],
    ) -> list[RecognizerResult]:
        """Convert our Entity objects to Presidio's RecognizerResult format.

        Args:
            entities: List of entities to convert

        Returns:
            List of Presidio RecognizerResult objects
        """
        return [
            RecognizerResult(
                entity_type=entity.type,
                start=entity.start,
                end=entity.end,
                score=entity.score,
            )
            for entity in entities
        ]
