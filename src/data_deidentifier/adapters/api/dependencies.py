from typing import Annotated

from fastapi import Depends, Request
from logger import LoggerContract

from src.data_deidentifier.adapters.infrastructure.config.contract import ConfigContract
from src.data_deidentifier.adapters.presidio.analyzer.analyzer import PresidioAnalyzer
from src.data_deidentifier.ports.analyzer_port import AnalyzerPort


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

    This dependency creates a new Presidio analyzer instance for each request.

    Args:
        logger: The logger instance obtained via dependency injection

    Returns:
        An implementation of the analyzer port
    """
    return PresidioAnalyzer(
        logger=logger,
    )
