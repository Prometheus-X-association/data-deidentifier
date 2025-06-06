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
        # Extract text segment
        start = result.start
        end = result.end
        entity_text = (
            text[start:end] if text and start is not None and end is not None else None
        )

        return Entity(
            type=result.entity_type,
            start=start,
            end=end,
            score=result.score,
            text=entity_text,
        )
