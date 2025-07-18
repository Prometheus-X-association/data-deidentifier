# Anonymization API

This page documents the anonymization services, types, and implementations.

## Services

Application services that orchestrate the anonymization process.

### Text Anonymization Service

::: domain.services.anonymization.text.TextAnonymizationService
    options:
      heading_level: 4

### Structured Data Anonymization Service

::: domain.services.anonymization.structured.StructuredDataAnonymizationService
    options:
      heading_level: 4

## Domain Types

Core types and enums used by the anonymization system.

### Entity

::: domain.types.entity.Entity
    options:
      heading_level: 4

### Anonymization Operator

::: domain.types.anonymization_operator.AnonymizationOperator
    options:
      heading_level: 4
      show_if_no_docstring: true

### Supported Language

::: domain.types.language.SupportedLanguage
    options:
      heading_level: 4
      show_if_no_docstring: true

## Result Types

Data structures returned by anonymization operations.

### Text Anonymization Result

::: domain.types.text_anonymization_result.TextAnonymizationResult
    options:
      heading_level: 4

### Structured Data Anonymization Result

::: domain.types.structured_anonymization_result.StructuredDataAnonymizationResult
    options:
      heading_level: 4

### Structured Data Analysis Field

::: domain.types.structured_anonymization_result.StructuredDataAnalysisField
    options:
      heading_level: 4

## Contracts

Abstract interfaces that define the anonymization behavior.

### Text Anonymizer Contract

::: domain.contracts.anonymizer.text.TextAnonymizerContract
    options:
      heading_level: 4

### Structured Data Anonymizer Contract

::: domain.contracts.anonymizer.structured.StructuredDataAnonymizerContract
    options:
      heading_level: 4

## Presidio Implementations

Concrete implementations using Microsoft Presidio.

### Text Anonymizer

::: adapters.presidio.anonymizer.text.PresidioTextAnonymizer
    options:
      heading_level: 4

### Structured Data Anonymizer

::: adapters.presidio.anonymizer.structured.PresidioStructuredDataAnonymizer
    options:
      heading_level: 4

## API Layer

FastAPI routes and data validation schemas.

### Request/Response Schemas

::: adapters.api.anonymize.schemas
    options:
      heading_level: 4
      show_signature_annotations: true
      show_if_no_docstring: true

### Router

::: adapters.api.anonymize.router
    options:
      heading_level: 4

