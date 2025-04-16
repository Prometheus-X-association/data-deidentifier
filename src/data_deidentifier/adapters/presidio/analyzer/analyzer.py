from typing import override

from logger import LoggerContract
from presidio_analyzer import AnalyzerEngine, RecognizerResult

from src.data_deidentifier.adapters.presidio.types.entities import PresidioEntityType
from src.data_deidentifier.domain.exceptions import (
    AnalyzationError,
    UnknownEntityTypeError,
)
from src.data_deidentifier.domain.types.entities import Entity, EntityType
from src.data_deidentifier.ports.analyzer_port import AnalyzerPort


class PresidioAnalyzer(AnalyzerPort):
    """Implementation of the analyzer port using Microsoft Presidio.

    This class uses the Presidio Analyzer to detect PII entities in text.
    """

    def __init__(self, logger: LoggerContract) -> None:
        """Initialize the Presidio analyzer.

        Args:
            logger: Logger for logging events
        """
        self.logger = logger

        self.analyzer = AnalyzerEngine()

        self.logger.debug("Presidio Analyzer initialized successfully")

    @override
    def analyze(
        self,
        text: str,
        language: str,
        entity_types: list[EntityType] | None = None,
        min_score: float = 0.5,
    ) -> list[Entity]:
        logger_context = {"text_length": len(text), "language": language}
        self.logger.debug("Starting text analysis", logger_context)

        try:
            presidio_results = self.analyzer.analyze(
                text=text,
                language=language,
                entities=entity_types,
                score_threshold=min_score,
            )
        except Exception as e:
            msg = "Unexpected error during entity recognition"
            self.logger.exception(
                "Unexpected error during entity recognition",
                e,
                logger_context,
            )
            raise AnalyzationError(msg) from e

        results = []
        for result in presidio_results:
            entity = self._recognizer_result_to_entity(result=result, text=text)
            results.append(entity)

        self.logger.info(
            "Analysis completed successfully",
            {"entities_found": len(results), **logger_context},
        )

        return results

    def _recognizer_result_to_entity(
        self,
        result: RecognizerResult,
        text: str,
    ) -> Entity:
        """Convert a Presidio RecognizerResult to our Entity model.

        Args:
            result: Presidio's analysis result
            text: Original text (to extract the entity text)

        Returns:
            Entity object with our model

        Raises:
            UnknownEntityTypeError: If entity type is not recognized
        """
        result_dict = result.to_dict()
        self.logger.debug("Analysis result", result_dict)

        entity_type_str = result_dict.get("entity_type")
        try:
            entity_type = PresidioEntityType(entity_type_str)
        except ValueError as e:
            msg = "Unknown entity type"
            self.logger.exception(msg, e, result_dict)
            raise UnknownEntityTypeError(msg) from e

        # Extract text segment
        start = result_dict.get("start")
        end = result_dict.get("end")
        entity_text = (
            text[start:end] if text and start is not None and end is not None else None
        )

        return Entity(
            type=entity_type,
            start=start,
            end=end,
            score=result_dict.get("score"),
            text=entity_text,
        )
