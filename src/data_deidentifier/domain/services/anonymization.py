from src.data_deidentifier.domain.contracts.anonymizer import AnonymizerContract
from src.data_deidentifier.domain.contracts.validator import EntityTypeValidatorContract
from src.data_deidentifier.domain.types.anonymization_operator import (
    AnonymizationOperator,
)
from src.data_deidentifier.domain.types.anonymization_result import AnonymizationResult


class AnonymizationService:
    """Service for anonymizing personally identifiable information in text.

    This service orchestrates the text anonymization process, manages default values,
    and produces structured anonymization results.
    """

    def __init__(
        self,
        anonymizer: AnonymizerContract,
        validator: EntityTypeValidatorContract,
    ) -> None:
        """Initialize the anonymizer service.

        Args:
            anonymizer: Implementation of the anonymizer contract
            validator: Implementation of the validator contract
        """
        self.anonymizer = anonymizer
        self.validator = validator

    def anonymize_text(
        self,
        text: str,
        operator: AnonymizationOperator,
        language: str,
        min_score: float,
        entity_types: list[str],
    ) -> AnonymizationResult:
        """Anonymize PII entities in text.

        Args:
            text: The text to anonymize
            operator: Anonymization method to use
            language: Language code of the text
            min_score: Minimum confidence score
            entity_types: Entity types to detect

        Returns:
            An AnonymizationResult containing the anonymized text and metadata
        """
        # Validate data
        effective_entity_types = self.validator.validate_entity_types(
            entity_types=entity_types,
        )

        # Anonymize the text
        return self.anonymizer.anonymize_text(
            text=text,
            operator=operator,
            entity_types=effective_entity_types,
            language=language,
            min_score=min_score,
        )
