from presidio_analyzer import RecognizerResult

from src.data_deidentifier.domain.types.entity import Entity


class PresidioEntityMapper:
    """Handles the conversion between domain entities and Presidio's formats."""

    @staticmethod
    def presidio_result_to_entity(result: RecognizerResult, text: str) -> Entity:
        """Convert a Presidio RecognizerResult to our Entity model.

        Args:
            result: Presidio's analysis result
            text: Original text (to extract the entity text)

        Returns:
            Entity object with our model
        """
        result_dict = result.to_dict()

        # Extract text segment
        start = result_dict.get("start")
        end = result_dict.get("end")
        entity_text = (
            text[start:end] if text and start is not None and end is not None else None
        )

        return Entity(
            type=result_dict.get("entity_type"),
            start=start,
            end=end,
            score=result_dict.get("score"),
            text=entity_text,
        )

    @staticmethod
    def entity_to_presidio_result(entity: Entity) -> RecognizerResult:
        """Convert our Entity model to Presidio's RecognizerResult format.

        Args:
            entity: Entity object with our model

        Returns:
            Presidio's analysis result
        """
        return RecognizerResult(
            entity_type=entity.type,
            start=entity.start,
            end=entity.end,
            score=entity.score,
        )
