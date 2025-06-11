from typing import Annotated, override

from configcore import Settings as CoreSettings
from pydantic import BeforeValidator, Field

from src.data_deidentifier.domain.types.anonymization_operator import (
    AnonymizationOperator,
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
