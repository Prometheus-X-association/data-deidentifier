from typing import Annotated

from fastapi import Depends, Request
from logger import LoggerContract

from src.data_deidentifier.adapters.infrastructure.config.contract import ConfigContract
from src.data_deidentifier.adapters.presidio.anonymizer.anonymizer import (
    PresidioAnonymizer,
)
from src.data_deidentifier.adapters.presidio.validator import PresidioValidator
from src.data_deidentifier.domain.contracts.anonymizer import AnonymizerContract
from src.data_deidentifier.domain.contracts.validator import EntityTypeValidatorContract


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


async def get_anonymizer(
    logger: Annotated[LoggerContract, Depends(get_logger)],
) -> AnonymizerContract:
    """Create and return an anonymizer instance.

    Args:
        logger: The logger instance

    Returns:
        An implementation of the anonymizer contract
    """
    return PresidioAnonymizer(
        logger=logger,
    )


async def get_validator(
    logger: Annotated[LoggerContract, Depends(get_logger)],
) -> EntityTypeValidatorContract:
    """Create and return an entity type validator instance.

    Args:
        logger: The logger instance

    Returns:
        An implementation of the entity type validator contract
    """
    return PresidioValidator(
        logger=logger,
    )
