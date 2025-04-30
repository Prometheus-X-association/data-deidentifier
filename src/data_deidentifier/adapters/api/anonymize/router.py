from typing import Annotated

from fastapi import APIRouter, Depends

from src.data_deidentifier.adapters.api.dependencies import (
    get_analyzer,
    get_anonymizer,
    get_config,
    get_validator,
)
from src.data_deidentifier.adapters.api.mapper import ApiEntityMapper
from src.data_deidentifier.adapters.infrastructure.config.contract import ConfigContract
from src.data_deidentifier.domain.contracts.analyzer import AnalyzerContract
from src.data_deidentifier.domain.contracts.anonymizer import AnonymizerContract
from src.data_deidentifier.domain.contracts.validator import EntityTypeValidatorContract
from src.data_deidentifier.domain.services.analyze import AnalyzeService
from src.data_deidentifier.domain.services.anonymization import AnonymizationService

from .schemas import (
    AnonymizeTextRequest,
    AnonymizeTextResponse,
)

router = APIRouter(prefix="/anonymize")


@router.post(
    "/text",
    tags=["Data anonymization"],
    summary="Anonymize text content for PII entities",
    status_code=200,
)
async def anonymize_text(
    query: AnonymizeTextRequest,
    anonymizer: Annotated[AnonymizerContract, Depends(get_anonymizer)],
    analyzer: Annotated[AnalyzerContract, Depends(get_analyzer)],
    validator: Annotated[EntityTypeValidatorContract, Depends(get_validator)],
    config: Annotated[ConfigContract, Depends(get_config)],
) -> AnonymizeTextResponse:
    """Anonymize PII entities in text content.

    If entities are not provided, the text will be analyzed first to detect them.

    Args:
        query: The request containing text to anonymize
        anonymizer: The anonymizer implementation
        analyzer: The analyzer implementation, needed if entities are not provided
        validator: The validator implementation
        config: The application configuration

    Returns:
        Anonymized text and information about the entities that were anonymized
    """
    anonymize_service = AnonymizationService(
        anonymizer=anonymizer,
        validator=validator,
        default_operator=config.get_default_anonymization_operator(),
    )

    text = query.text

    if query.entities:
        # Convert provided API entities to domain entities
        entities = [ApiEntityMapper.adapter_to_domain(e) for e in query.entities]
    else:
        # Retrieve entities via analyze service
        analyze_service = AnalyzeService(
            analyzer=analyzer,
            validator=validator,
            default_language=config.get_default_language(),
            default_min_score=config.get_default_minimum_score(),
            default_entity_types=config.get_default_entity_types(),
        )

        analysis_result = analyze_service.analyze_text(
            text=query.text,
            language=query.language,
            min_score=query.min_score,
            entity_types=query.entity_types,
        )

        entities = analysis_result.entities

    # Anonymize the text
    result = anonymize_service.anonymize_text(
        text=text,
        entities=entities,
        operator=query.operator,
    )

    return AnonymizeTextResponse(
        anonymized_text=result.anonymized_text,
        meta={
            "operator": result.operator,
            "entities": result.entity_stats,
        },
    )
