from typing import override

from configcore import Settings as CoreSettings
from pydantic import Field

from .contract import ConfigContract


class Settings(CoreSettings, ConfigContract):
    """Application settings loaded from environment variables, via Pydantic model."""

    default_language: str = Field(default="en")

    default_minimum_score: float = Field(default=0.5, ge=0.0, le=1.0)

    @override
    def get_default_language(self) -> str:
        return self.default_language

    @override
    def get_default_minimum_score(self) -> float:
        return self.default_minimum_score
