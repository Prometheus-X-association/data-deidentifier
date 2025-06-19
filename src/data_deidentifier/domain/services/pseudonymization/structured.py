from typing import Any

from src.data_deidentifier.domain.contracts.pseudonymizer.structured import (
    StructuredDataPseudonymizerContract,
)
from src.data_deidentifier.domain.contracts.validator import EntityTypeValidatorContract
from src.data_deidentifier.domain.exceptions import (
    InvalidInputDataError,
)
from src.data_deidentifier.domain.types.pseudonymization_method import (
    PseudonymizationMethod,
)
from src.data_deidentifier.domain.types.structured_data import StructuredData
from src.data_deidentifier.domain.types.structured_pseudonymization_result import (
    StructuredDataPseudonymizationResult,
)


class StructuredDataPseudonymizationService:
    """Service for pseudonymizing personally identifiable information in data.

    This service orchestrates the structured data pseudonymization process
    and produces structured pseudonymization results.
    """

    def __init__(
        self,
        pseudonymizer: StructuredDataPseudonymizerContract,
        validator: EntityTypeValidatorContract,
    ) -> None:
        """Initialize the structured data pseudonymization service.

        Args:
            pseudonymizer: Implementation of the data pseudonymization contract
            validator: Implementation of the validator contract
        """
        self.pseudonymizer = pseudonymizer
        self.validator = validator

    def pseudonymize(
        self,
        data: StructuredData,
        method: PseudonymizationMethod,
        language: str,
        entity_types: list[str],
        method_params: dict[str, Any] | None = None,
    ) -> StructuredDataPseudonymizationResult:
        """Anonymize PII entities in text.

        Args:
            data: The structured data to anonymize
            method: Pseudonymization method to use
            language: Language code of the text
            entity_types: Entity types to detect
            method_params: Optional parameters for the method

        Returns:
            A StructuredDataPseudonymizationResult
            containing the pseudonymized data and metadata
        """
        if not data:
            raise InvalidInputDataError("Data cannot be empty")

        # Validate data
        effective_entity_types = self.validator.validate_entity_types(
            entity_types=entity_types,
        )

        # Pseudonymize the text
        return self.pseudonymizer.pseudonymize(
            data=data,
            method=method,
            method_params=method_params,
            entity_types=effective_entity_types,
            language=language,
        )
