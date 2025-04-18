from typing import override

from src.data_deidentifier.adapters.api.schemas import EntityResponse
from src.data_deidentifier.adapters.presidio.types.entities import PresidioEntityType
from src.data_deidentifier.domain.exceptions import UnknownEntityTypeError
from src.data_deidentifier.domain.types.entities import Entity
from src.data_deidentifier.ports.mapper_port import EntityMapperPort


class PresidioEntityMapper(EntityMapperPort):
    """Implementation of the entity mapper port for Microsoft Presidio.

    This class provides bidirectional conversion between domain entity models
    and both API response models and Presidio-specific entity formats.
    """

    @override
    def domain_to_api(self, entity: Entity) -> EntityResponse:
        return EntityResponse(
            type=entity.type.value,
            start=entity.start,
            end=entity.end,
            score=entity.score,
            text=entity.text,
            path=entity.path,
        )

    @override
    def api_to_domain(self, entity_response: EntityResponse) -> Entity:
        try:
            entity_type = PresidioEntityType(entity_response.type)
        except ValueError as e:
            raise UnknownEntityTypeError(
                f"Unknown entity type: {entity_response.type}",
            ) from e

        return Entity(
            type=entity_type,
            start=entity_response.start,
            end=entity_response.end,
            score=entity_response.score,
            text=entity_response.text,
            path=entity_response.path,
        )
