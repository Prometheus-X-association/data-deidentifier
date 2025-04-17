from src.data_deidentifier.adapters.api.schemas import EntityResponse
from src.data_deidentifier.domain.types.entities import Entity


class EntityMapper:
    """Utility class for mapping between domain entities and API models.

    This class provides static methods to convert domain objects into their
    API representation counterparts, following the separation of concerns
    principle by isolating conversion logic from model definitions.
    """

    @staticmethod
    def entity_to_response(entity: Entity) -> EntityResponse:
        """Convert a domain Entity to an API EntityResponse.

        This method transforms an internal domain entity into the format
        expected in the API response.

        Args:
            entity: The domain entity to convert

        Returns:
            The converted entity response object
        """
        return EntityResponse(
            entity_type=entity.type.value,
            start=entity.start,
            end=entity.end,
            score=entity.score,
            text=entity.text,
            path=entity.path,
        )
