from dataclasses import dataclass

from .structured_anonymization_result import StructuredDataAnalysisField
from .structured_data import StructuredData


@dataclass
class StructuredDataPseudonymizationResult:
    """Result of a structured data pseudonymization operation.

    This class encapsulates all information about a pseudonymization operation.

    Attributes:
        pseudonymized_data: The structured data after pseudonymization
        detected_fields: List of fields with detected PII entities
    """

    pseudonymized_data: StructuredData
    detected_fields: list[StructuredDataAnalysisField]

    @property
    def field_mapping(self) -> dict[str, str]:
        """Get field mapping as a dictionary for convenience."""
        return {field.field_name: field.entity_type for field in self.detected_fields}
