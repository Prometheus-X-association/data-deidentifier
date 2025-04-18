from typing import Annotated

from fastapi import APIRouter, Depends

from src.data_deidentifier.adapters.api.dependencies import (
    get_analyzer,
    get_config,
    get_mapper,
)
from src.data_deidentifier.adapters.infrastructure.config.contract import ConfigContract
from src.data_deidentifier.ports.analyzer_port import AnalyzerPort
from src.data_deidentifier.ports.mapper_port import EntityMapperPort

from .schemas import (
    AnalyzeTextRequest,
    AnalyzeTextResponse,
)

router = APIRouter(prefix="/analyze")


@router.post(
    "/text",
    tags=["Data anonymization"],
    summary="Analyze text for PII entities",
    status_code=200,
)
async def analyze_text(
    query: AnalyzeTextRequest,
    analyzer: Annotated[AnalyzerPort, Depends(get_analyzer)],
    mapper: Annotated[EntityMapperPort, Depends(get_mapper)],
    config: Annotated[ConfigContract, Depends(get_config)],
) -> AnalyzeTextResponse:
    """Analyze text content for PII entities.

    This endpoint analyzes the provided text to detect personally identifiable
    information (PII) entities such as names, email addresses, phone numbers, etc.

    Args:
        query: The request query model containing the text to analyze
        analyzer: The analyzer implementation
        mapper: The entity mapper implementation
        config: The application configuration

    Returns:
        Analysis results containing the detected entities and statistics
    """
    language = query.language or config.get_default_language()
    min_score = (
        query.min_score
        if query.min_score is not None
        else config.get_default_minimum_score()
    )
    input_text = query.text

    entities = analyzer.analyze_text(
        text=input_text,
        language=language,
        min_score=min_score,
    )

    entity_responses = []
    type_stats = {}  # Number of entity type occurrences
    for entity in entities:
        # Convert domain entities to API entities for response
        entity_responses.append(mapper.domain_to_api(entity))

        entity_type = str(entity.type)
        type_stats[entity_type] = type_stats.get(entity_type, 0) + 1

    return AnalyzeTextResponse(
        entities=entity_responses,
        meta={
            "language": language,
            "min_score": min_score,
            "entities": type_stats,
        },
    )
