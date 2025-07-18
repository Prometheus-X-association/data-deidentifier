from enum import StrEnum, auto


class EnrichmentType(StrEnum):
    """Enumeration of supported pseudonym enricher types.

    Attributes:
        HTTP: HTTP-based enricher that calls external web services to obtain
            enrichment information. Requires URL configuration and supports
            timeouts and retry logic.
    """

    HTTP = auto()
