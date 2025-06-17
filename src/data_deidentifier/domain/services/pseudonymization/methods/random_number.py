import secrets
from typing import Any, override

from src.data_deidentifier.domain.contracts.pseudonymizer.method import (
    PseudonymizationMethodContract,
)
from src.data_deidentifier.domain.types.entity import Entity


class RandomNumberPseudonymizationMethod(PseudonymizationMethodContract):
    """Random number pseudonymization method with intra-request consistency."""

    FORMAT = "<{entity_type}_{number}>"
    RANDOM_BITS_NUMBER = 24

    def __init__(self, params: dict[str, Any] | None = None) -> None:
        """Initialize the random method.

        Args:
            params: Method parameters (seed, format, etc.)
        """
        super().__init__(params=params)

        # Cache by entity type and text
        self._mapping: dict[str, dict[str, str]] = {}

    @override
    def generate_pseudonym(self, entity: Entity) -> str:
        cache_key = entity.text

        # Mapping by entity type
        entity_type = entity.type
        if entity_type not in self._mapping:
            self._mapping[entity_type] = {}

        # Check if we already have a pseudonym for this entity
        entity_mapping_for_type = self._mapping.get(entity_type)
        if cache_key in entity_mapping_for_type:
            return entity_mapping_for_type.get(cache_key)

        # Generate base random number
        random_number = secrets.randbits(self.RANDOM_BITS_NUMBER)

        # Format the pseudonym
        pseudonym = f"<{entity_type}_{random_number}>"

        # Store for consistency
        self._mapping[entity_type][cache_key] = pseudonym
        return pseudonym
