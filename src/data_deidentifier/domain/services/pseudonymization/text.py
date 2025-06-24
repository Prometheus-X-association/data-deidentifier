from typing import Any

from logger import LoggerContract

from src.data_deidentifier.domain.contracts.pseudonymizer.text import (
    TextPseudonymizerContract,
)
from src.data_deidentifier.domain.contracts.validator import EntityTypeValidatorContract
from src.data_deidentifier.domain.exceptions import (
    InvalidInputTextError,
    TextPseudonymizationError,
)
from src.data_deidentifier.domain.services.pseudonymization.methods.factory import (
    PseudonymizationMethodFactory,
)
from src.data_deidentifier.domain.types.pseudonymization_method import (
    PseudonymizationMethod,
)
from src.data_deidentifier.domain.types.text_pseudonymization_result import (
    TextPseudonymizationResult,
)


class TextPseudonymizationService:
    """Service for pseudonymizing personally identifiable information in text.

    This service orchestrates the text pseudonymization process
    and produces structured pseudonymization results.
    """

    def __init__(
        self,
        pseudonymizer: TextPseudonymizerContract,
        validator: EntityTypeValidatorContract,
        logger: LoggerContract,
    ) -> None:
        """Initialize the text pseudonymization service.

        Args:
            pseudonymizer: Implementation of the text pseudonymization contract
            validator: Implementation of the validator contract
            logger: Logger for logging events
        """
        self.pseudonymizer = pseudonymizer
        self.validator = validator
        self.logger = logger

    def pseudonymize(  # noqa: PLR0913
        self,
        text: str,
        method: PseudonymizationMethod,
        language: str,
        min_score: float,
        entity_types: list[str],
        method_params: dict[str, Any] | None = None,
    ) -> TextPseudonymizationResult:
        """Pseudonymize PII entities in text.

        Args:
            text: The text to pseudonymize
            method: Pseudonymization method to use
            language: Language code of the text
            min_score: Minimum confidence score
            entity_types: Entity types to detect
            method_params: Optional parameters for the method

        Returns:
            A TextPseudonymizationResult containing the pseudonymized text and metadata

        Raises:
            InvalidInputTextError: If the data is empty
            TextPseudonymizationError: If the method is unknown
        """
        if not text or not text.strip():
            raise InvalidInputTextError("Text cannot be empty")

        # Get the pseudonymization method
        try:
            method_instance = PseudonymizationMethodFactory.create(
                method=method,
                method_params=method_params or {},
                logger=self.logger,
            )
        except Exception as e:
            raise TextPseudonymizationError(
                "Pseudonymization method loading failed",
            ) from e

        # Validate data
        effective_entity_types = self.validator.validate_entity_types(
            entity_types=entity_types,
        )

        # Pseudonymize the text
        return self.pseudonymizer.pseudonymize(
            text=text,
            method=method_instance,
            entity_types=effective_entity_types,
            language=language,
            min_score=min_score,
        )
