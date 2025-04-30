from typing import Annotated

from fastapi import APIRouter, Depends

from src.data_deidentifier.adapters.api.dependencies import (
    get_analyzer,
    get_config,
    get_validator,
)
from src.data_deidentifier.adapters.api.mapper import ApiEntityMapper
from src.data_deidentifier.adapters.infrastructure.config.contract import ConfigContract
from src.data_deidentifier.domain.contracts.analyzer import AnalyzerContract
from src.data_deidentifier.domain.contracts.validator import EntityTypeValidatorContract
from src.data_deidentifier.domain.services.analyze import AnalyzeService

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
    analyzer: Annotated[AnalyzerContract, Depends(get_analyzer)],
    validator: Annotated[EntityTypeValidatorContract, Depends(get_validator)],
    config: Annotated[ConfigContract, Depends(get_config)],
) -> AnalyzeTextResponse:
    """Analyze text content for PII entities.

    This endpoint analyzes the provided text to detect personally identifiable
    information (PII) entities such as names, email addresses, phone numbers, etc.

    Args:
        query: The request query model containing the text to analyze
        analyzer: The analyzer implementation
        validator: The validator implementation
        config: The application configuration

    Returns:
        Analysis results containing the detected entities and statistics
    """
    service = AnalyzeService(
        analyzer=analyzer,
        validator=validator,
        default_language=config.get_default_language(),
        default_min_score=config.get_default_minimum_score(),
        default_entity_types=config.get_default_entity_types(),
    )

    analysis_result = service.analyze_text(
        text=query.text,
        language=query.language,
        min_score=query.min_score,
        entity_types=query.entity_types,
    )

    entities = [
        ApiEntityMapper.domain_to_adapter(entity=e) for e in analysis_result.entities
    ]

    return AnalyzeTextResponse(
        entities=entities,
        meta={
            "language": analysis_result.language,
            "min_score": analysis_result.min_score,
            "entities": analysis_result.entity_stats,
        },
    )
