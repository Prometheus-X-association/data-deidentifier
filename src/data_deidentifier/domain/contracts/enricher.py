from abc import ABC, abstractmethod

from src.data_deidentifier.domain.types.entity import Entity


class EntityEnricherContract(ABC):
    """Contract for entity enrichment services.

    Defines the interface for services that provide additional contextual information
    for detected PII entities that enhance the output while maintaining privacy.
    """

    @abstractmethod
    def get_enrichment(self, entity: Entity) -> str | None:
        """Get enrichment information for a detected entity.

        Analyzes the provided entity and returns contextual information that can
        be safely included with the result without compromising privacy.

        Args:
            entity: The detected PII entity to enrich. Contains the entity text,
                type, confidence score, and position information.

        Returns:
            str | None: Enrichment information as a string if available.

        Raises:
            EntityEnrichmentError: If an error while enriching occurs.

        Examples:
            >>> entity = Entity(text="London", type="LOCATION", ...)
            >>> enricher.get_enrichment(entity)
            "United Kingdom"
        """
        raise NotImplementedError
