from typing import Annotated, override

from configcore import Settings as CoreSettings
from pydantic import BeforeValidator, Field

from src.data_deidentifier.domain.types.anonymization_operator import (
    AnonymizationOperator,
)
from src.data_deidentifier.domain.types.pseudonymization_method import (
    PseudonymizationMethod,
)

from .contract import ConfigContract


class Settings(CoreSettings, ConfigContract):
    """Application settings loaded from environment variables, via Pydantic model."""

    default_language: str = Field(default="en")

    default_minimum_score: float = Field(default=0.5, ge=0.0, le=1.0)

    default_entity_types: list[str] = Field(default_factory=list)

    default_anonymization_operator: Annotated[
        AnonymizationOperator,
        BeforeValidator(
            lambda v: AnonymizationOperator[v.upper()] if isinstance(v, str) else v,
        ),
    ] = Field(
        default=AnonymizationOperator.REPLACE,
    )

    default_pseudonymization_method: Annotated[
        PseudonymizationMethod,
        BeforeValidator(
            lambda v: PseudonymizationMethod[v.upper()] if isinstance(v, str) else v,
        ),
    ] = Field(
        default=PseudonymizationMethod.RANDOM_NUMBER,
    )

    enrichment_enabled: bool = Field(default=False)
    enrichment_timeout: int = Field(default=10, ge=1, le=60)

    # URL mappings for entity enrichment (JSON string format)
    # Example: '{"LOCATION": "https://api.example.com/location"}' # noqa: ERA001
    enrichment_url_mappings: dict[str, str] = Field(default_factory=dict)

    @override
    def get_default_language(self) -> str:
        return self.default_language

    @override
    def get_default_minimum_score(self) -> float:
        return self.default_minimum_score

    @override
    def get_default_entity_types(self) -> list[str]:
        return self.default_entity_types

    @override
    def get_default_anonymization_operator(self) -> AnonymizationOperator:
        return self.default_anonymization_operator

    @override
    def get_default_pseudonymization_method(self) -> PseudonymizationMethod:
        return self.default_pseudonymization_method

    @override
    def get_enrichment_enabled(self) -> bool:
        return self.enrichment_enabled

    @override
    def get_enrichment_url_mappings(self) -> dict[str, str]:
        return self.enrichment_url_mappings

    @override
    def get_enrichment_timeout_seconds(self) -> int:
        return self.enrichment_timeout
