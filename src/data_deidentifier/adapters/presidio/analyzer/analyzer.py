from typing import override

from logger import LoggerContract
from presidio_analyzer import AnalyzerEngine

from src.data_deidentifier.adapters.presidio.mapper import PresidioEntityMapper
from src.data_deidentifier.domain.contracts.analyzer import AnalyzerContract
from src.data_deidentifier.domain.exceptions import AnalyzationError
from src.data_deidentifier.domain.types.entity import Entity


class PresidioAnalyzer(AnalyzerContract):
    """Implementation of the analyzer contract using Microsoft Presidio.

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
    def analyze_text(
        self,
        text: str,
        language: str,
        min_score: float,
        entity_types: list[str] | None = None,
    ) -> list[Entity]:
        logger_context = {
            "text_length": len(text),
            "language": language,
            "min_score": min_score,
            "entity_types": entity_types,
        }
        self.logger.debug("Starting text analysis", logger_context)

        try:
            # Analyze text
            presidio_results = self.analyzer.analyze(
                text=text,
                language=language,
                score_threshold=min_score,
                entities=entity_types,
            )
        except Exception as e:
            msg = "Unexpected error during entity recognition"
            self.logger.exception(
                "Unexpected error during entity recognition",
                e,
                logger_context,
            )
            raise AnalyzationError(msg) from e

        # Convert results to our format
        results = [
            PresidioEntityMapper.presidio_result_to_entity(
                result=result,
                text=text,
            )
            for result in presidio_results
        ]

        self.logger.info(
            "Analysis completed successfully",
            {"entities_found": len(results), **logger_context},
        )

        return results
