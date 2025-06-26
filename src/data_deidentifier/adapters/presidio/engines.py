import threading
from typing import ClassVar

from logger import LoggerContract
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.operators.operators_factory import ANONYMIZERS
from presidio_structured import StructuredEngine
from presidio_structured.data.data_processors import DataProcessorBase

from .analyzer.structured_types.factory import (
    StructuredDataAnalyzerFactory,
)
from .pseudonymizer.custom_operator import (
    PseudonymizeOperator,
)


class PresidioEngineFactory:
    """Thread-safe factory and cache manager for Presidio engines.

    Provides a centralized way to lazily instantiate and reuse Presidio engines
    across multiple requests, with thread safety and optional cache management.

    Attributes:
        _lock: Thread lock for safe singleton creation.
        _text_analyzer_engine: Cached instance of the text analyzer engine.
        _text_anonymizer_engine: Cached instance of the text anonymizer engine.
        _structured_data_factory: Cached factory for structured data analyzers.
        _structured_data_engines: Cache of structured anonymizer engines
         keyed by processor name.
    """

    _lock: ClassVar[threading.Lock] = threading.Lock()
    _analyzer_engine: ClassVar[AnalyzerEngine | None] = None
    _text_anonymizer_engine: ClassVar[AnonymizerEngine | None] = None
    _structured_data_factory: ClassVar[StructuredDataAnalyzerFactory | None] = None
    _structured_data_engines: ClassVar[dict[str, StructuredEngine]] = {}

    @classmethod
    def get_analyzer_engine(cls) -> AnalyzerEngine:
        """Get a shared instance of the analyzer engine (thread-safe).

        Lazily initializes the `AnalyzerEngine` if not already created
        and returns the same instance for subsequent calls.

        Returns:
            AnalyzerEngine: The shared analyzer engine.
        """
        if cls._analyzer_engine is None:
            with cls._lock:
                if cls._analyzer_engine is None:
                    cls._analyzer_engine = AnalyzerEngine()
        return cls._analyzer_engine

    @classmethod
    def get_text_anonymizer_engine(cls) -> AnonymizerEngine:
        """Get a shared instance of the text anonymizer engine (thread-safe).

        Lazily initializes the `AnonymizerEngine` if not already created
        and returns the same instance for subsequent calls.

        Returns:
            AnonymizerEngine: The shared text anonymizer engine.
        """
        if cls._text_anonymizer_engine is None:
            with cls._lock:
                if cls._text_anonymizer_engine is None:
                    cls._text_anonymizer_engine = AnonymizerEngine()
                    cls._text_anonymizer_engine.add_anonymizer(PseudonymizeOperator)
        return cls._text_anonymizer_engine

    @classmethod
    def get_structured_data_analyzer_factory(
        cls,
        logger: LoggerContract,
    ) -> StructuredDataAnalyzerFactory:
        """Get a shared instance of the structured data analyzer factory (thread-safe).

        Lazily initializes the `StructuredDataAnalyzerFactory` if not already created
        and returns the same instance for future calls.

        Args:
            logger (LoggerContract): Logger instance to be used by the factory.

        Returns:
            StructuredDataAnalyzerFactory: The shared factory for data analyzers.
        """
        if cls._structured_data_factory is None:
            with cls._lock:
                if cls._structured_data_factory is None:
                    cls._structured_data_factory = StructuredDataAnalyzerFactory(logger)
        return cls._structured_data_factory

    @classmethod
    def get_structured_data_anonymizer_engine(
        cls,
        processor: DataProcessorBase,
    ) -> StructuredEngine:
        """Get a cached structured data anonymizer engine for a given data processor.

        Returns a StructuredEngine instance based on the processor's type.
        If an engine for the given processor type does not exist in the cache,
        it is created and stored for future reuse (thread-safe).

        Args:
            processor: The data processor used to configure the anonymizer engine.

        Returns:
            StructuredEngine: A structured anonymizer engine for the given processor.
        """
        key = type(processor).__name__

        if key not in cls._structured_data_engines:
            with cls._lock:
                if key not in cls._structured_data_engines:
                    # Adding pseudonymization operator to Presidio's operator list
                    # Issue :
                    # StructuredEngine -> DataProcessorBase._generate_operator_mapping()
                    # instantiates a new OperatorsFactory(), which only loads
                    # predefined operators from the global ANONYMIZERS list.
                    if PseudonymizeOperator not in ANONYMIZERS:
                        ANONYMIZERS.append(PseudonymizeOperator)

                    cls._structured_data_engines[key] = StructuredEngine(
                        data_processor=processor,
                    )

        return cls._structured_data_engines[key]
