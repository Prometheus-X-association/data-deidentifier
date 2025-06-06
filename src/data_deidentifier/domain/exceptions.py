class DataDeidentifierError(Exception):
    """Base class for all exceptions in data-deidentifier."""


class EntityTypeValidationError(DataDeidentifierError):
    """Raised when entity types validation fails."""


class AnonymizationError(DataDeidentifierError):
    """Raised when an error occurs during the anonymization process."""
