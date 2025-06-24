from abc import abstractmethod

from configcore import ConfigContract as CoreConfigContract

from src.data_deidentifier.domain.types.anonymization_operator import (
    AnonymizationOperator,
)
from src.data_deidentifier.domain.types.pseudonymization_method import (
    PseudonymizationMethod,
)


class ConfigContract(CoreConfigContract):
    """Contract for application configuration."""

    @abstractmethod
    def get_default_language(self) -> str:
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
        raise NotImplementedError

    @abstractmethod
    def get_enrichment_enabled(self) -> bool:
        """Check if entity enrichment is enabled.

        Returns:
            bool: True if entity enrichment is enabled, False otherwise.
        """
        raise NotImplementedError

    @abstractmethod
    def get_enrichment_url_mappings(self) -> dict[str, str]:
        """Get the URL mappings for entity enrichment services.

        Returns:
            dict[str, str]: A mapping of entity types to their corresponding
                enrichment service URLs. Keys are entity types (e.g., 'LOCATION')
                and values are HTTP endpoints for enrichment.
        """
        raise NotImplementedError

    @abstractmethod
    def get_enrichment_timeout_seconds(self) -> int:
        """Get the timeout for enrichment HTTP requests.

        Returns:
            int: The timeout in seconds for HTTP requests to enrichment services.
        """
        raise NotImplementedError
