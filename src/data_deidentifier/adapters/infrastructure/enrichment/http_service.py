from typing import override

from logger import LoggerContract

from src.data_deidentifier.adapters.infrastructure.config.contract import ConfigContract
from src.data_deidentifier.adapters.infrastructure.http.client import (
    BaseHttpClient,
    HttpClientError,
)
from src.data_deidentifier.domain.contracts.enricher import PseudonymEnricherContract
from src.data_deidentifier.domain.exceptions import PseudonymEnrichmentError
from src.data_deidentifier.domain.types.entity import Entity


class HttpPseudonymEnricher(PseudonymEnricherContract):
    """HTTP client specifically for entity enrichment services.

    Provides a higher-level interface for making enrichment requests by wrapping
    the base HTTP client with enrichment-specific logic and error handling.
    """

    def __init__(self, config: ConfigContract, logger: LoggerContract) -> None:
        """Initialize the enrichment HTTP client.

        Args:
            config: Configuration contract providing enrichment settings
            logger: Logger instance for recording enrichment operations
        """
        self.config = config
        self.logger = logger

        self.http_client = BaseHttpClient(logger)

    @override
    def get_enrichment(self, entity: Entity) -> str | None:
        url_mappings = self.config.get_enrichment_url_mappings()
        if entity.type not in url_mappings:
            return None

        url = url_mappings.get(entity.type)
        entity_text = entity.text

        logger_context = {
            "entity_type": entity.type,
            "url": url,
        }
        self.logger.debug("Starting enrichment", logger_context)

        try:
            response = self.http_client.request(
                url=url,
                method="POST",
                data={"text": entity_text},
                timeout_seconds=self.config.get_enrichment_timeout_seconds(),
            )

            data = response.json()
            enrichment = data.get("text")

            if enrichment and isinstance(enrichment, str) and enrichment.strip():
                self.logger.debug(
                    "Pseudonym enrichment successful",
                    {"enrichment": enrichment},
                )
                return enrichment

            self.logger.debug("No enrichment returned by service", logger_context)

        except HttpClientError as e:
            # Transform generic HTTP error into enrichment-specific context
            raise PseudonymEnrichmentError from e
        except Exception as e:
            # Handle JSON parsing errors, etc.
            self.logger.warning(
                "Pseudonym enrichment processing failed",
                {"error": str(e), **logger_context},
            )
            raise PseudonymEnrichmentError from e

        return None
