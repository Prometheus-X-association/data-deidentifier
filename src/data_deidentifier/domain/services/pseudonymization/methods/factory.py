from typing import Any, ClassVar

from src.data_deidentifier.domain.contracts.pseudonymizer.method import (
    PseudonymizationMethodContract,
)
from src.data_deidentifier.domain.exceptions import TextPseudonymizationError
from src.data_deidentifier.domain.types.pseudonymization_method import (
    PseudonymizationMethod,
)


class PseudonymizationMethodFactory:
    """Factory for creating pseudonymization method instances."""

    # Mapping between method enums and implementation classes
    _METHOD_MAPPING: ClassVar[
        dict[PseudonymizationMethod, type[PseudonymizationMethodContract]]
    ] = {}

    @classmethod
    def create(
        cls,
        method: PseudonymizationMethod,
        params: dict[str, Any] | None = None,
    ) -> PseudonymizationMethodContract:
        """Create a pseudonymization method instance.

        Args:
            method: The pseudonymization method enum
            params: Parameters for the method

        Returns:
            A method instance implementing PseudonymizationMethodContract

        Raises:
            TextPseudonymizationError: If method is not supported
        """
        if method not in cls._METHOD_MAPPING:
            raise TextPseudonymizationError(
                f"Unsupported pseudonymization method: {method}. "
                f"Supported methods: {cls.get_supported_methods()}",
            )

        method_class = cls._METHOD_MAPPING[method]
        return method_class(params=params)

    @classmethod
    def get_supported_methods(cls) -> list[PseudonymizationMethod]:
        """Get list of supported pseudonymization methods.

        Returns:
            List of supported methods
        """
        return list(cls._METHOD_MAPPING.keys())
