from typing import Any, override

from logger import LoggerContract

from src.data_deidentifier.adapters.infrastructure.http.client import (
    BaseHttpClient,
    HttpClientError,
)
from src.data_deidentifier.domain.contracts.enricher.enricher import (
    PseudonymEnricherContract,
)
from src.data_deidentifier.domain.exceptions import PseudonymEnrichmentError
from src.data_deidentifier.domain.types.entity import Entity


class HttpPseudonymEnricher(PseudonymEnricherContract):
    """HTTP client specifically for entity enrichment services.

    Provides a higher-level interface for making enrichment requests by wrapping
    the base HTTP client with enrichment-specific logic and error handling.
    """

    PARAM_URL = "url"
    PARAM_TIMEOUT = "timeout"

    @override
    def __init__(self, params: dict[str, Any], logger: LoggerContract) -> None:
        super().__init__(params=params, logger=logger)

        self.http_client = BaseHttpClient(logger)

    @override
    def get_enrichment(self, entity: Entity) -> str | None:
        if self.PARAM_URL not in self.params:
            return None
        url = self.params.get(self.PARAM_URL)
        entity_text = entity.text

        logger_context = {
            "entity_type": entity.type,
            "url": url,
        }
        self.logger.debug("Starting pseudonym enrichment via HTTP", logger_context)

        try:
            response = self.http_client.request(
                url=url,
                method="POST",
                data={"text": entity_text},
                timeout_seconds=self.params.get(self.PARAM_TIMEOUT),
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
