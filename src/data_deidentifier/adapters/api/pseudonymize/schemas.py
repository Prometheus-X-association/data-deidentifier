from typing import Any

from pydantic import BaseModel, Field

from src.data_deidentifier.domain.types.entity import Entity
from src.data_deidentifier.domain.types.language import SupportedLanguage
from src.data_deidentifier.domain.types.pseudonymization_method import (
    PseudonymizationMethod,
)


class PseudonymizeTextRequest(BaseModel):
    """Request model for pseudonymizing text.

    This model defines the input parameters for the text pseudonymization endpoint.
    """

    text: str = Field(..., description="The text content to pseudonymize")

    method: PseudonymizationMethod | None = Field(
        default=None,
        description="Pseudonymization method",
    )

    method_params: dict[str, Any] | None = Field(
        default=None,
        description="Pseudonymization method parameters",
    )

    language: SupportedLanguage | None = Field(
        default=None,
        description="Language code of the text (e.g., 'en', 'fr', 'es')",
    )

    min_score: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Minimum confidence score threshold (0.0 to 1.0)",
    )

    entity_types: list[str] | None = Field(
        default=None,
        description="Types of entities to detect (defaults to all supported types)",
    )


class PseudonymizeTextResponse(BaseModel):
    """Response model for text pseudonymization.

    This model defines the structure of the response
    returned by the text pseudonymization endpoint.
    """

    pseudonymized_text: str = Field(..., description="The pseudonymized text content")

    detected_entities: list[Entity] = Field(
        ...,
        description="List of detected PII entities",
    )

    meta: dict[str, Any] | None = Field(
        default_factory=dict,
        description="Statistics about the pseudonymization operation",
    )
