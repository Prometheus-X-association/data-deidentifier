from typing import override

from src.data_deidentifier.adapters.api.response import EntityResponse
from src.data_deidentifier.domain.contracts.mapper import EntityMapperContract
from src.data_deidentifier.domain.types.entity import Entity


class ApiEntityMapper(EntityMapperContract[EntityResponse]):
    """Implementation of the presentation mapper contract for REST API.

    This class converts between domain entities and API response models,
    ensuring proper data formatting for external API communication.
    """

    @override
    def domain_to_adapter(self, entity: Entity) -> EntityResponse:
        return EntityResponse(
            type=entity.type,
            start=entity.start,
            end=entity.end,
            score=entity.score,
            text=entity.text,
            path=entity.path,
        )

    @override
    def adapter_to_domain(self, entity_response: EntityResponse) -> Entity:
        return Entity(
            type=entity_response.type,
            start=entity_response.start,
            end=entity_response.end,
            score=entity_response.score,
            text=entity_response.text,
            path=entity_response.path,
        )
