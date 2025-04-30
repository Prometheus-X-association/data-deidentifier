from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from src.data_deidentifier.domain.types.entity import Entity

AdapterEntity = TypeVar("AdapterEntity")


class EntityMapperContract(ABC, Generic[AdapterEntity]):
    """Contract for mapping between domain entities and external representations.

    This contract defines how domain entities are converted to and from
    presentation formats intended for external interfaces, regardless
    of their nature (API, CLI, UI, etc.).

    Type Parameters:
        T: The type of external representation
    """

    @staticmethod
    @abstractmethod
    def domain_to_adapter(entity: Entity) -> AdapterEntity:
        """Convert a domain Entity to an adapter entity.

        This method transforms an internal domain entity
        into the format expected in the domain response.

        Args:
            entity: The domain entity to convert

        Returns:
            The converted entity response object
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def adapter_to_domain(entity_response: AdapterEntity) -> Entity:
        """Convert an adapter entity to a domain entity.

        This method transforms an adapter Entity into the internal domain format.

        Args:
            entity_response: The adapter entity to convert

        Returns:
            The converted domain entity object
        """
        raise NotImplementedError
