from enum import StrEnum


class UpperStrEnum(StrEnum):
    """A string enum that automatically converts names to uppercase values."""

    @staticmethod
    def _generate_next_value_(
        name: str,
        _start: int,
        _count: int,
        _last_values: list[str],
    ) -> str:
        """Generate the next enum value by converting the member name to uppercase."""
        return name.upper()
