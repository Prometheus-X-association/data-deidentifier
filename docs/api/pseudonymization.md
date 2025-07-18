# Pseudonymization API

This page documents the pseudonymization services, methods, enrichment capabilities, and implementations.

## Services

Application services that orchestrate the pseudonymization process.

### Text Pseudonymization Service

::: domain.services.pseudonymization.text.TextPseudonymizationService
    options:
      heading_level: 4

### Structured Data Pseudonymization Service

::: domain.services.pseudonymization.structured.StructuredDataPseudonymizationService
    options:
      heading_level: 4

## Domain Types

Core types and enums used by the pseudonymization system.

### Pseudonymization Method

::: domain.types.pseudonymization_method.PseudonymizationMethod
    options:
      heading_level: 4
      show_if_no_docstring: true

### Enrichment Type

::: domain.types.enrichment_type.EnrichmentType
    options:
      heading_level: 4
      show_if_no_docstring: true

## Result Types

Data structures returned by pseudonymization operations.

### Text Pseudonymization Result

::: domain.types.text_pseudonymization_result.TextPseudonymizationResult
    options:
      heading_level: 4

### Structured Data Pseudonymization Result

::: domain.types.structured_pseudonymization_result.StructuredDataPseudonymizationResult
    options:
      heading_level: 4

## Pseudonymization Methods

Concrete implementations of pseudonymization algorithms.

### Method Factory

::: domain.services.pseudonymization.methods.factory.PseudonymizationMethodFactory
    options:
      heading_level: 4

### Random Number Method

::: domain.services.pseudonymization.methods.random_number.RandomNumberPseudonymizationMethod
    options:
      heading_level: 4

### Counter Method

::: domain.services.pseudonymization.methods.counter.CounterPseudonymizationMethod
    options:
      heading_level: 4

### Crypto Hash Method

::: domain.services.pseudonymization.methods.crypto_hash.CryptoHashPseudonymizationMethod
    options:
      heading_level: 4

## Entity Enrichment

External service integration for adding contextual information to pseudonyms.

### Enrichment Manager Contract

::: domain.contracts.enricher.manager.PseudonymEnrichmentManagerContract
    options:
      heading_level: 4

### Enrichment Factory

::: adapters.infrastructure.enrichment.factory.EnrichmentFactory
    options:
      heading_level: 4

### HTTP Enrichment Service

::: adapters.infrastructure.enrichment.http_service.HttpPseudonymEnricher
    options:
      heading_level: 4

## Contracts

Abstract interfaces that define the pseudonymization behavior.

### Text Pseudonymizer Contract

::: domain.contracts.pseudonymizer.text.TextPseudonymizerContract
    options:
      heading_level: 4

### Structured Data Pseudonymizer Contract

::: domain.contracts.pseudonymizer.structured.StructuredDataPseudonymizerContract
    options:
      heading_level: 4

### Pseudonymization Method Contract

::: domain.contracts.pseudonymizer.method.PseudonymizationMethodContract
    options:
      heading_level: 4

### Pseudonym Enricher Contract

::: domain.contracts.enricher.enricher.PseudonymEnricherContract
    options:
      heading_level: 4

## Presidio Implementations

Concrete implementations using Microsoft Presidio with custom pseudonymization.

### Text Pseudonymizer

::: adapters.presidio.pseudonymizer.text.PresidioTextPseudonymizer
    options:
      heading_level: 4

### Structured Data Pseudonymizer

::: adapters.presidio.pseudonymizer.structured.PresidioStructuredDataPseudonymizer
    options:
      heading_level: 4

### Custom Pseudonymize Operator

::: adapters.presidio.pseudonymizer.custom_operator.PseudonymizeOperator
    options:
      heading_level: 4

## API Layer

FastAPI routes and data validation schemas for pseudonymization.

### Request/Response Schemas

::: adapters.api.pseudonymize.schemas
    options:
      heading_level: 4
      show_signature_annotations: true
      show_if_no_docstring: true

### Router Functions

::: adapters.api.pseudonymize.router
    options:
      heading_level: 4
