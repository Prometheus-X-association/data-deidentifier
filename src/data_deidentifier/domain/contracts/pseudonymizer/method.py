from abc import ABC, abstractmethod
from typing import Any

from src.data_deidentifier.domain.types.entity import Entity


class PseudonymizationMethodContract(ABC):
    """Contract for pseudonymization methods."""

    def __init__(self, params: dict[str, Any] | None = None) -> None:
        """Initialize the pseudonymization method.

        Args:
            params: Optional parameters for the method configuration
        """
        self.params = params or {}

    @abstractmethod
    def generate_pseudonym(self, entity: Entity) -> str:
        """Generate a pseudonym for an entity.

        Args:
            entity: The original entity

        Returns:
            A pseudonym for the entity
        """
        raise NotImplementedError
