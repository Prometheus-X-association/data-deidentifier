import threading
from typing import Any, override

from src.data_deidentifier.domain.contracts.pseudonymizer.method import (
    PseudonymizationMethodContract,
)
from src.data_deidentifier.domain.types.entity import Entity


class CounterPseudonymizationMethod(PseudonymizationMethodContract):
    """Counter pseudonymization method with intra-request consistency."""

    PARAM_START_NUMBER = "start_number"
    DEFAULT_START_NUMBER = 1

    def __init__(self, params: dict[str, Any] | None = None) -> None:
        """Initialize the counter method.

        Args:
            params: Method parameters (seed, format, etc.)
        """
        super().__init__(params=params)

        # Cache by entity type and text
        self._mapping: dict[str, dict[str, str]] = {}

        # Counters by entity_type
        self._counters: dict[str, int] = {}

        # Configuration
        self._start_number = self.params.get(
            self.PARAM_START_NUMBER,
            self.DEFAULT_START_NUMBER,
        )

        # Thread safety for concurrent access
        self._lock = threading.Lock()

    @override
    def generate_pseudonym(self, entity: Entity) -> str:
        cache_key = entity.text
        entity_type = entity.type

        with self._lock:
            # Mapping by entity type
            if entity_type not in self._mapping:
                self._mapping[entity_type] = {}
                self._counters[entity_type] = self._start_number
            else:
                # Check if we already have a pseudonym for this entity
                entity_mapping_for_type = self._mapping.get(entity_type)
                if cache_key in entity_mapping_for_type:
                    return entity_mapping_for_type.get(cache_key)

        # Generate new pseudonym with current counter
        current_count = self._counters.get(entity_type)
        pseudonym = f"<{entity_type}_{current_count}>"

        # Store for consistency
        self._mapping[entity_type][cache_key] = pseudonym
        self._counters[entity_type] += 1
        return pseudonym
