from typing import Any

from pydantic import BaseModel, Field

from src.data_deidentifier.adapters.api.schemas import EntityResponse


class AnalyzeTextRequest(BaseModel):
    """Request model for analyzing text.

    This model defines the input parameters for the text analysis endpoint.
    """

    text: str = Field(..., description="The text content to analyze")

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


class AnalyzeTextResponse(BaseModel):
    """Response model for text analysis.

    This model defines the structure of the response
    returned by the text analysis endpoint.
    """

    entities: list[EntityResponse] = Field(
        ...,
        description="The entities found in the content",
    )

    meta: dict[str, Any] | None = Field(
        default_factory=dict,
        description="Statistics about the analysis",
    )
