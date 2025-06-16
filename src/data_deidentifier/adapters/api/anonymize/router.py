from typing import Annotated

from fastapi import APIRouter, Depends

from src.data_deidentifier.adapters.api.dependencies import (
    get_config,
    get_structured_anonymizer,
    get_text_anonymizer,
    get_validator,
)
from src.data_deidentifier.adapters.infrastructure.config.contract import ConfigContract
from src.data_deidentifier.domain.contracts.anonymizer.structured import (
    StructuredDataAnonymizerContract,
)
from src.data_deidentifier.domain.contracts.anonymizer.text import (
    TextAnonymizerContract,
)
from src.data_deidentifier.domain.contracts.validator import EntityTypeValidatorContract
from src.data_deidentifier.domain.services.anonymization.structured import (
    StructuredDataAnonymizationService,
)
from src.data_deidentifier.domain.services.anonymization.text import (
    TextAnonymizationService,
)

from .schemas import (
    AnonymizeStructuredDataRequest,
    AnonymizeStructuredDataResponse,
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
    anonymizer: Annotated[TextAnonymizerContract, Depends(get_text_anonymizer)],
    validator: Annotated[EntityTypeValidatorContract, Depends(get_validator)],
    config: Annotated[ConfigContract, Depends(get_config)],
) -> AnonymizeTextResponse:
    """Anonymize PII entities in text content.

    Args:
        query: The request containing text to anonymize
        anonymizer: The text anonymizer implementation
        validator: The validator implementation
        config: The application configuration

    Returns:
        Anonymized text and information about the entities that were anonymized
    """
    effective_operator = query.operator or config.get_default_anonymization_operator()
    effective_language = query.language or config.get_default_language()
    effective_min_score = (
        query.min_score
        if query.min_score is not None
        else config.get_default_minimum_score()
    )
    effective_entity_types = query.entity_types or config.get_default_entity_types()

    anonymize_service = TextAnonymizationService(
        anonymizer=anonymizer,
        validator=validator,
    )

    result = anonymize_service.anonymize(
        text=query.text,
        operator=effective_operator,
        operator_params=query.operator_params,
        language=effective_language,
        min_score=effective_min_score,
        entity_types=effective_entity_types,
    )

    return AnonymizeTextResponse(
        anonymized_text=result.anonymized_text,
        detected_entities=result.detected_entities,
        meta={
            "operator": effective_operator,
            "language": effective_language,
            "min_score": effective_min_score,
        },
    )


@router.post(
    "/structured",
    tags=["Structured data anonymization"],
    summary="Anonymize structured data for PII entities",
    status_code=200,
)
async def anonymize_structured(
    query: AnonymizeStructuredDataRequest,
    anonymizer: Annotated[
        StructuredDataAnonymizerContract,
        Depends(get_structured_anonymizer),
    ],
    validator: Annotated[EntityTypeValidatorContract, Depends(get_validator)],
    config: Annotated[ConfigContract, Depends(get_config)],
) -> AnonymizeStructuredDataResponse:
    """Anonymize PII entities in structured data.

    Args:
        query: The request containing structured data to anonymize
        anonymizer: The structured data anonymizer implementation
        validator: The validator implementation
        config: The application configuration

    Returns:
        Anonymized structured data and information about the fields that were anonymized
    """
    effective_operator = query.operator or config.get_default_anonymization_operator()
    effective_language = query.language or config.get_default_language()
    effective_entity_types = query.entity_types or config.get_default_entity_types()

    anonymize_service = StructuredDataAnonymizationService(
        anonymizer=anonymizer,
        validator=validator,
    )

    result = anonymize_service.anonymize(
        data=query.data,
        operator=effective_operator,
        operator_params=query.operator_params,
        language=effective_language,
        entity_types=effective_entity_types,
    )

    return AnonymizeStructuredDataResponse(
        anonymized_data=result.anonymized_data,
        detected_fields=result.field_mapping,
        meta={
            "operator": effective_operator,
            "language": effective_language,
        },
    )
