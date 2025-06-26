from logger import LoggerContract
from presidio_analyzer import AnalyzerEngine, RecognizerResult

from src.data_deidentifier.adapters.presidio.exceptions import AnalyzeError


class PresidioAnalyzer:
    """Uses the Presidio Analyzer to detect PII entities in text."""

    def __init__(self, logger: LoggerContract) -> None:
        """Initialize the Presidio analyzer.

        Args:
            logger: Logger for logging events
        """
        self.logger = logger

        self.presidio_analyzer = AnalyzerEngine()

        self.logger.debug("Presidio Analyzer initialized successfully")

    def analyze_text(
        self,
        text: str,
        language: str,
        min_score: float,
        entity_types: list[str] | None = None,
    ) -> list[RecognizerResult]:
        """Analyze text to detect PII entities.

        Args:
            text: Text to analyze
            language: Language code of the text
            min_score: Minimum confidence score threshold
            entity_types: Types of entities to detect (None means all supported types)

        Returns:
            List of detected entities

        Raises:
            AnalyzeError: If analysis fails
        """
        language = language.lower()

        logger_context = {
            "text_length": len(text),
            "language": language,
            "min_score": min_score,
            "entity_types": entity_types,
        }
        self.logger.debug("Starting text analysis", logger_context)

        try:
            # Analyze text
            presidio_results = self.presidio_analyzer.analyze(
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
            raise AnalyzeError(msg) from e

        self.logger.info(
            "Analysis completed successfully",
            {"entities_found": len(presidio_results), **logger_context},
        )

        return presidio_results
