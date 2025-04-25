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
        description="Pre-identified entities (if None, text will be analyzed first)",
    )

    operator: AnonymizationOperator = Field(
        default=AnonymizationOperator.REPLACE,
        description="Anonymization method",
    )

    language: str | None = Field(
        default=None,
        description="Language code of the text (for analysis phase)",
    )

    min_score: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Minimum confidence score threshold (for analysis phase)",
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
