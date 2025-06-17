from typing import TYPE_CHECKING

from presidio_anonymizer.operators import Operator, OperatorType

from src.data_deidentifier.domain.types.anonymization_operator import (
    AnonymizationOperator,
)
from src.data_deidentifier.domain.types.entity import Entity

if TYPE_CHECKING:
    from src.data_deidentifier.domain.contracts.pseudonymizer.method import (
        PseudonymizationMethodContract,
    )


class PseudonymizeOperator(Operator):
    """Custom Presidio operator for pseudonymization."""

    PARAM_METHOD: str = "method"

    def operate(self, text: str, params: dict | None = None) -> str:
        """Generate a pseudonym for the entity.

        Args:
            text: The original entity text
            params: Parameters containing method, entity_type, etc.

        Returns:
            The pseudonymized text
        """
        method: PseudonymizationMethodContract = params.get(self.PARAM_METHOD)

        entity = Entity(
            text=text,
            type=params.get("entity_type"),
            start=params.get("start", 0),
            end=params.get("end", len(text)),
            score=params.get("score", 1.0),
        )

        return method.generate_pseudonym(entity=entity)

    def validate(self, params: dict | None = None) -> None:
        """Validate operator parameters."""
        if not params:
            raise ValueError("Parameters are required")

        if self.PARAM_METHOD not in params:
            raise ValueError("A 'method' parameter is required")

        if "entity_type" not in params:
            raise ValueError("A 'entity_type' parameter is required")

    def operator_name(self) -> str:
        """Return operator name."""
        return AnonymizationOperator.PSEUDONYMIZE.value

    def operator_type(self) -> OperatorType:
        """Return operator type."""
        return OperatorType.Anonymize
