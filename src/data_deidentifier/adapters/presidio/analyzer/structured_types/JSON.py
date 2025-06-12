from typing import Any, override

from presidio_structured import (
    JsonAnalysisBuilder,
    StructuredAnalysis,
)
from presidio_structured.data.data_processors import (
    DataProcessorBase,
    JsonDataProcessor,
)

from src.data_deidentifier.domain.exceptions import InvalidInputDataError

from .structured_type import StructuredTypeAnalyzer


class JsonAnalyzer(StructuredTypeAnalyzer):
    """Analyzer for JSON data.

    This class implements analysis for JSON-formatted data (Python dictionaries)
    using Presidio's JsonAnalysisBuilder.
    """

    @override
    def can_handle(self, data: Any) -> bool:
        return isinstance(data, dict)

    @override
    def analyze(self, data: Any, language: str) -> StructuredAnalysis:
        if not self.can_handle(data=data):
            raise InvalidInputDataError("Data must be a dict")

        self.logger.debug("Analyzing JSON data", {"nb_keys": len(data)})

        analyzer = JsonAnalysisBuilder()
        return analyzer.generate_analysis(
            data=data,
            language=language,
        )

    @override
    def get_data_processor(self) -> DataProcessorBase:
        return JsonDataProcessor()
