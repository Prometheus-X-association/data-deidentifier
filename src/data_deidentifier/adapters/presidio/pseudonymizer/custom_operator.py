from typing import TYPE_CHECKING

from presidio_anonymizer.operators import Operator, OperatorType

from src.data_deidentifier.domain.exceptions import PseudonymEnrichmentError
from src.data_deidentifier.domain.types.anonymization_operator import (
    AnonymizationOperator,
)
from src.data_deidentifier.domain.types.entity import Entity

if TYPE_CHECKING:
    from src.data_deidentifier.domain.contracts.enricher import (
        PseudonymEnricherContract,
    )
    from src.data_deidentifier.domain.contracts.pseudonymizer.method import (
        PseudonymizationMethodContract,
    )


class PseudonymizeOperator(Operator):
    """Custom Presidio operator for pseudonymization with optional enrichment.

    This operator extends Presidio's anonymization capabilities by providing
    pseudonymization instead of simple redaction or masking. It generates
    consistent pseudonyms for entities and optionally enriches them with
    contextual information.

    Attributes:
        PARAM_METHOD: Parameter key for the pseudonymization method.
        PARAM_ENRICHER: Parameter key for the optional pseudonym enricher.

    Examples:
        Input text: "John lives in London"
        Output: "<PERSON_123> lives in <LOCATION_456> (United Kingdom)"
    """

    PARAM_METHOD: str = "method"
    PARAM_ENRICHER: str = "enricher"
    PARAM_ENRICHABLE_TYPES = "enrichable_types"
    ENRICHMENT_FORMAT = ""

    def operate(self, text: str, params: dict | None = None) -> str:
        """Generate a pseudonym for the entity, using a PseudonymizationMethodContract.

        Args:
            text: The original entity text
            params: Parameters containing method, entity_type, etc.

        Returns:
            The pseudonymized text
        """
        method: PseudonymizationMethodContract = params.get(self.PARAM_METHOD)

        enrichable_types = params.get(self.PARAM_ENRICHABLE_TYPES, set())
        enricher: PseudonymEnricherContract | None = params.get(self.PARAM_ENRICHER)

        entity = Entity(
            text=text,
            type=params.get("entity_type"),
            start=params.get("start", 0),
            end=params.get("end", len(text)),
            score=params.get("score", 1.0),
        )

        pseudonym = method.generate_pseudonym(entity=entity)

        if enricher and enrichable_types and entity.type in enrichable_types:
            try:
                enrichment = enricher.get_enrichment(entity)
            except PseudonymEnrichmentError:
                enrichment = None

            if enrichment:
                pseudonym = f"{pseudonym} ({enrichment})"

        return pseudonym

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
