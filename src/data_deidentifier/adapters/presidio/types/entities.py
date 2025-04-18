# ruff: noqa: ERA001

from enum import auto

from src.data_deidentifier.domain.types.entities import EntityType
from src.data_deidentifier.domain.utils.utils_enum import UpperStrEnum


class PresidioEntityType(EntityType, UpperStrEnum):
    """Enumeration of the types of PII entities that can be detected by Presidio.

    This enum extends the base EntityType to define all entity types that
    can be detected by the Microsoft Presidio analyzer.
    """

    # Common PII entity types
    PERSON = auto()
    LOCATION = auto()
    DATE_TIME = auto()
    NRP = auto()  # Nationality, religious or political group

    # Predefined recognizers
    EMAIL_ADDRESS = auto()
    PHONE_NUMBER = auto()
    CREDIT_CARD = auto()
    IP_ADDRESS = auto()
    URL = auto()
    IBAN_CODE = auto()
    MEDICAL_LICENSE = auto()
    CRYPTO = auto()

    # US-specific recognizers
    # US_SSN = auto()
    # US_BANK_NUMBER = auto()
    # US_DRIVER_LICENSE = auto()
    # US_ITIN = auto()
    # US_PASSPORT = auto()

    # # UK-specific recognizers
    # UK_NHS = auto()
    # UK_NINO = auto()

    # # Other country-specific recognizers
    # AU_ABN = auto()
    # AU_ACN = auto()
    # AU_TFN = auto()
    # AU_MEDICARE = auto()

    # IT_FISCAL_CODE = auto()
    # IT_DRIVER_LICENSE = auto()
    # IT_VAT_CODE = auto()
    # IT_PASSPORT = auto()
    # IT_IDENTITY_CARD = auto()

    # ES_NIF = auto()
    # ES_NIE = auto()

    # # Indian recognizers
    # IN_PAN = auto()
    # IN_AADHAAR = auto()
    # IN_VOTER = auto()
    # IN_PASSPORT = auto()
    # IN_VEHICLE_REGISTRATION = auto()

    # # Others
    # SG_NRIC_FIN = auto()
    # SG_UEN = auto()
    # FI_PERSONAL_IDENTITY_CODE = auto()
    # PL_PESEL = auto()
