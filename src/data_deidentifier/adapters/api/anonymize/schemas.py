from typing import Any

from pydantic import BaseModel, Field

from src.data_deidentifier.adapters.api.response import EntityResponse
from src.data_deidentifier.domain.types.operators import AnonymizationOperator


class AnonymizeTextRequest(BaseModel):
    """Request model for anonymizing text.

    This model defines the input parameters for the text anonymization endpoint.
    """

    text: str = Field(..., description="The text content to anonymize")

    entities: list[EntityResponse] | None = Field(
        default_factory=list,
        description="Pre-identified entities (if empty, text will be analyzed first)",
    )

    operator: AnonymizationOperator | None = Field(
        default=None,
        description="Anonymization method",
    )

    language: str | None = Field(
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


class AnonymizeTextResponse(BaseModel):
    """Response model for text anonymization.

    This model defines the structure of the response
    returned by the text anonymization endpoint.
    """

    anonymized_text: str = Field(..., description="The anonymized text content")

    meta: dict[str, Any] | None = Field(
        default_factory=dict,
        description="Statistics about anonymized entity types",
    )
