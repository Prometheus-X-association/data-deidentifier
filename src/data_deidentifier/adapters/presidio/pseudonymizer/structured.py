from typing import Any, override

from logger import LoggerContract

from src.data_deidentifier.adapters.presidio.anonymizer.structured import (
    PresidioStructuredDataAnonymizer,
)
from src.data_deidentifier.domain.contracts.pseudonymizer.structured import (
    StructuredDataPseudonymizerContract,
)
from src.data_deidentifier.domain.exceptions import (
    StructuredDataAnonymizationError,
    StructuredDataPseudonymizationError,
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
from src.data_deidentifier.domain.types.structured_data import StructuredData
from src.data_deidentifier.domain.types.structured_pseudonymization_result import (
    StructuredDataPseudonymizationResult,
)

from .custom_operator import PseudonymizeOperator


class PresidioStructuredDataPseudonymizer(StructuredDataPseudonymizerContract):
    """Implementation of data pseudonymizer contract using Microsoft Presidio."""

    def __init__(self, logger: LoggerContract) -> None:
        """Initialize the Presidio structured data pseudonymizer.

        Args:
            logger: Logger for logging events
        """
        self.logger = logger

        self.anonymizer = PresidioStructuredDataAnonymizer(logger=self.logger)

        self.logger.debug("Presidio data Pseudonymizer initialized successfully")

    @override
    def pseudonymize(
        self,
        data: StructuredData,
        method: PseudonymizationMethod,
        language: str,
        entity_types: list[str] | None = None,
        method_params: dict[str, Any] | None = None,
    ) -> StructuredDataPseudonymizationResult:
        logger_context = {
            "method": method.value,
        }
        self.logger.debug("Starting data pseudonymization", logger_context)

        # Get the pseudonymization method
        try:
            pseudonymization_method = PseudonymizationMethodFactory.create(
                method=method,
                method_params=method_params or {},
                logger=self.logger,
            )
        except Exception as e:
            raise StructuredDataPseudonymizationError(
                "Pseudonymization method loading failed",
            ) from e

        # Delegate to anonymizer with our custom operator
        try:
            anonymization_result = self.anonymizer.anonymize(
                data=data,
                operator=AnonymizationOperator.PSEUDONYMIZE,
                language=language,
                entity_types=entity_types,
                operator_params={
                    PseudonymizeOperator.PARAM_METHOD: pseudonymization_method,
                },
            )
        except StructuredDataAnonymizationError as e:
            raise StructuredDataPseudonymizationError(
                "Pseudonymization failed during anonymization",
            ) from e

        self.logger.info("Data pseudonymization completed successfully", logger_context)

        # Adapt the result
        return StructuredDataPseudonymizationResult(
            pseudonymized_data=anonymization_result.anonymized_data,
            detected_fields=anonymization_result.detected_fields,
        )
