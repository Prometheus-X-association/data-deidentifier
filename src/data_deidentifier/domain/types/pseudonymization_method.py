from enum import StrEnum, auto


class PseudonymizationMethod(StrEnum):
    """Enumeration for pseudonymization methods."""

    RANDOM_NUMBER = auto()
    COUNTER = auto()
    CRYPTO_HASH = auto()
