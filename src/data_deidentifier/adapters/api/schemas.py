from typing import Any

from pydantic import BaseModel, Field

from src.data_deidentifier.domain.types.entities import Entity


class AnalyzeTextRequest(BaseModel):
    """Request model for analyzing text.

    This model defines the input parameters for the text analysis endpoint.

    Attributes:
        text: The text content to analyze for PII entities
    """

    text: str = Field(..., description="The text content to analyze")


class EntityResponse(BaseModel):
    """Response model for an entity found in the content.

    This model represents a PII entity detected in the analyzed content
    formatted for API response.
    """

    entity_type: str = Field(..., description="The type of PII entity detected")
    start: int = Field(
        ...,
        description="The start position of the entity in the content",
    )
    end: int = Field(..., description="The end position of the entity in the content")
    score: float = Field(..., description="The confidence score of the detection")
    text: str = Field(..., description="The text of the entity")
    path: str | None = Field(
        None,
        description="The path to the field containing the entity (for JSON data)",
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
    stats: dict[str, Any] | None = Field(
        default_factory=dict,
        description="Statistics about the analysis",
    )

    @staticmethod
    def entity_to_response(entity: Entity) -> EntityResponse:
        """Convert a domain Entity to an API EntityResponse.

        This method transforms an internal domain entity into the format
        expected in the API response.

        Args:
            entity: The domain entity to convert

        Returns:
            The converted entity response object
        """
        return EntityResponse(
            entity_type=str(entity.type),
            start=entity.start,
            end=entity.end,
            score=entity.score,
            text=entity.text or "",
            path=entity.path,
        )
