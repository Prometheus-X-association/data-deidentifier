from abc import ABC, abstractmethod

from src.data_deidentifier.adapters.api.schemas import EntityResponse
from src.data_deidentifier.domain.types.entities import Entity


class EntityMapperPort(ABC):
    """Utility class for mapping between domain entities and API models.

    This class provides methods to convert domain objects into their
    API representation counterparts, following the separation of concerns
    principle by isolating conversion logic from model definitions.
    """

    @abstractmethod
    def domain_to_api(self, entity: Entity) -> EntityResponse:
        """Convert a domain Entity to an API EntityResponse.

        This method transforms an internal domain entity into the format
        expected in the API response.

        Args:
            entity: The domain entity to convert

        Returns:
            The converted entity response object
        """
        raise NotImplementedError

    @abstractmethod
    def api_to_domain(self, entity_response: EntityResponse) -> Entity:
        """Convert an API EntityResponse to a domain entity.

        This method transforms an API Entity into the internal domain format.

        Args:
            entity_response: The API entity to convert

        Returns:
            The converted domain entity object

        Raises:
            UnknownEntityTypeError: If entity type is not recognized
        """
        raise NotImplementedError
