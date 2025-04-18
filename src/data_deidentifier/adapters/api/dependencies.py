from typing import Annotated

from fastapi import Depends, Request
from logger import LoggerContract

from src.data_deidentifier.adapters.infrastructure.config.contract import ConfigContract
from src.data_deidentifier.adapters.presidio.analyzer.analyzer import PresidioAnalyzer
from src.data_deidentifier.adapters.presidio.anonymizer.anonymizer import (
    PresidioAnonymizer,
)
from src.data_deidentifier.adapters.presidio.mapper import PresidioEntityMapper
from src.data_deidentifier.ports.analyzer_port import AnalyzerPort
from src.data_deidentifier.ports.anonymizer_port import AnonymizerPort
from src.data_deidentifier.ports.mapper_port import EntityMapperPort


async def get_config(request: Request) -> ConfigContract:
    """Get the application configuration from the request state.

    Args:
        request: The FastAPI request object

    Returns:
        The application configuration
    """
    return request.state.config


async def get_logger(request: Request) -> LoggerContract:
    """Get the logger from the request state.

    Args:
        request: The FastAPI request object

    Returns:
        The logger instance
    """
    return request.state.logger


async def get_analyzer(
    logger: Annotated[LoggerContract, Depends(get_logger)],
) -> AnalyzerPort:
    """Create and return an analyzer instance.

    Args:
        logger: The logger instance obtained via dependency injection

    Returns:
        An implementation of the analyzer port
    """
    return PresidioAnalyzer(
        logger=logger,
    )


async def get_anonymizer(
    logger: Annotated[LoggerContract, Depends(get_logger)],
) -> AnonymizerPort:
    """Create and return an anonymizer instance.

    Args:
        logger: The logger instance

    Returns:
        An implementation of the anonymizer port
    """
    return PresidioAnonymizer(
        logger=logger,
    )


async def get_mapper() -> EntityMapperPort:
    """Create and return an mapper instance.

    Returns:
        An implementation of the mapper port
    """
    return PresidioEntityMapper()
