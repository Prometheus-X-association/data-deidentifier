from typing import Annotated

from fastapi import APIRouter, Depends

from src.data_deidentifier.adapters.api.dependencies import get_analyzer
from src.data_deidentifier.adapters.api.schemas import (
    AnalyzeTextRequest,
    AnalyzeTextResponse,
)
from src.data_deidentifier.ports.analyzer_port import AnalyzerPort

router = APIRouter(prefix="/analyze")


@router.post(
    "/text",
    tags=["Data anonymization"],
    summary="Analyze text for PII entities",
    status_code=200,
)
async def analyze(
    query: AnalyzeTextRequest,
    analyzer: Annotated[AnalyzerPort, Depends(get_analyzer)],
) -> AnalyzeTextResponse:
    """Analyze text content for PII entities.

    This endpoint analyzes the provided text to detect personally identifiable
    information (PII) entities such as names, email addresses, phone numbers, etc.

    Args:
        query: The request query model containing the text to analyze
        analyzer: The analyzer implementation, obtained via dependency injection

    Returns:
        Analysis results containing the detected entities and statistics
    """
    input_text = query.text
    entities = analyzer.analyze(text=input_text, language="en")

    entity_responses = [AnalyzeTextResponse.entity_to_response(e) for e in entities]
    return AnalyzeTextResponse(
        entities=entity_responses,
    )
