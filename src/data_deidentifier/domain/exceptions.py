class AnalyzeError(Exception):
    """Base class for all analysis-related exceptions."""


class AnalyzationError(AnalyzeError):
    """Raised when an error occurs during the analysis process."""


class AnonymizationError(Exception):
    """Raised when an error occurs during the anonymization process."""
