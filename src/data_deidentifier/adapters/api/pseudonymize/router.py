from typing import Annotated

from fastapi import APIRouter, Depends

from src.data_deidentifier.adapters.api.dependencies import (
    get_config,
    get_text_pseudonymizer,
    get_validator,
)
from src.data_deidentifier.adapters.infrastructure.config.contract import ConfigContract
from src.data_deidentifier.domain.contracts.pseudonymizer.text import (
    TextPseudonymizerContract,
)
from src.data_deidentifier.domain.contracts.validator import EntityTypeValidatorContract
from src.data_deidentifier.domain.services.pseudonymization.text import (
    TextPseudonymizationService,
)

from .schemas import PseudonymizeTextRequest, PseudonymizeTextResponse

router = APIRouter(prefix="/pseudonymize")


@router.post(
    "/text",
    tags=["Data pseudonymization"],
    summary="Pseudonymize text content for PII entities",
    status_code=200,
)
async def pseudonymize_text(
    query: PseudonymizeTextRequest,
    pseudonymizer: Annotated[
        TextPseudonymizerContract,
        Depends(get_text_pseudonymizer),
    ],
    validator: Annotated[EntityTypeValidatorContract, Depends(get_validator)],
    config: Annotated[ConfigContract, Depends(get_config)],
) -> PseudonymizeTextResponse:
    """Pseudonymize PII entities in text content.

    Args:
        query: The request containing text to pseudonymize
        pseudonymizer: The text pseudonymizer implementation
        validator: The validator implementation
        config: The application configuration

    Returns:
        Pseudonymized text and information about the entities that were pseudonymized
    """
    effective_method = query.method  # or config.get_default_pseudonymization_method()
    effective_language = query.language or config.get_default_language()
    effective_min_score = (
        query.min_score
        if query.min_score is not None
        else config.get_default_minimum_score()
    )
    effective_entity_types = query.entity_types or config.get_default_entity_types()

    pseudonymize_service = TextPseudonymizationService(
        pseudonymizer=pseudonymizer,
        validator=validator,
    )

    result = pseudonymize_service.pseudonymize(
        text=query.text,
        method=effective_method,
        method_params=query.method_params,
        language=effective_language,
        min_score=effective_min_score,
        entity_types=effective_entity_types,
    )

    return PseudonymizeTextResponse(
        pseudonymized_text=result.pseudonymized_text,
        detected_entities=result.detected_entities,
        meta={
            "method": effective_method,
            "language": effective_language,
            "min_score": effective_min_score,
        },
    )
