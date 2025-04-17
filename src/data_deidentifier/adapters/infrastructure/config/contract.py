from abc import abstractmethod

from configcore import ConfigContract as CoreConfigContract


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
