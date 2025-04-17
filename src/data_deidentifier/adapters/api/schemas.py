from pydantic import BaseModel, Field


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
