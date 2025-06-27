from abc import abstractmethod

from configcore import ConfigContract as CoreConfigContract

from src.data_deidentifier.domain.types.anonymization_operator import (
    AnonymizationOperator,
)
from src.data_deidentifier.domain.types.language import SupportedLanguage
from src.data_deidentifier.domain.types.pseudonymization_method import (
    PseudonymizationMethod,
)


class ConfigContract(CoreConfigContract):
    """Contract for application configuration."""

    @abstractmethod
    def get_default_language(self) -> SupportedLanguage:
        """Get the default language for text analysis.

        Returns:
            The default language code (e.g., 'en', 'fr')
        """
        raise NotImplementedError

    @abstractmethod
    def get_default_minimum_score(self) -> float:
        """Get the default minimum confidence score for entity detection.

        Returns:
            The default minimum score as a float between 0.0 and 1.0
        """
        raise NotImplementedError

    @abstractmethod
    def get_default_entity_types(self) -> list[str]:
        """Get the default entity types to detect.

        Returns:
            List of default entity types for text analysis.
        """
        raise NotImplementedError

    @abstractmethod
    def get_default_anonymization_operator(self) -> AnonymizationOperator:
        """Get the default anonymization operator.

        Returns:
            The default anonymization operator
        """
        raise NotImplementedError

    @abstractmethod
    def get_default_pseudonymization_method(self) -> PseudonymizationMethod:
        """Get the default pseudonymization method.

        Returns:
            The default pseudonymization method
        """
