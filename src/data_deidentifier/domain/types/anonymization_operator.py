from enum import StrEnum, auto


class AnonymizationOperator(StrEnum):
    """Enumeration for anonymization operators."""

    REPLACE = auto()
    REDACT = auto()
    MASK = auto()
    HASH = auto()
    ENCRYPT = auto()
