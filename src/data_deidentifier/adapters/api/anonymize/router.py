from typing import Annotated

from fastapi import APIRouter, Depends

from src.data_deidentifier.adapters.api.dependencies import (
    get_anonymizer,
    get_mapper,
)
from src.data_deidentifier.domain.contracts.anonymizer import AnonymizerContract
from src.data_deidentifier.domain.contracts.mapper import EntityMapperContract

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
    mapper: Annotated[EntityMapperContract, Depends(get_mapper)],
) -> AnonymizeTextResponse:
    """Anonymize PII entities in text content.

    If entities are not provided, the text will be analyzed first to detect them.

    Args:
        query: The request containing text to anonymize
        anonymizer: The anonymizer implementation
        mapper: The entity mapper implementation

    Returns:
        Anonymized text and information about the entities that were anonymized
    """
    text = query.text

    # Convert provided API entities to domain entities
    entities = [mapper.adapter_to_domain(e) for e in query.entities]

    # Anonymize the text
    anonymized_text = anonymizer.anonymize_text(
        text=text,
        entities=entities,
        operator=query.operator,
    )

    type_stats = {}  # Number of entity type occurrences
    for entity in entities:
        entity_type = str(entity.type)
        type_stats[entity_type] = type_stats.get(entity_type, 0) + 1

    return AnonymizeTextResponse(
        anonymized_text=anonymized_text,
        meta={
            "entities": type_stats,
        },
    )
