# Enterprise Data Normalization Pipeline

This module implements the core transformation and normalization pipeline for all data entering the Flood Guardian platform.

## Architecture
- **Schema Validator**: `validator.py` - Performs the first line of defense to ensure raw payloads are structurally intact.
- **Transformer**: `transformer.py` - Uses a Provider Registry to map arbitrary incoming field names (e.g., `temp`, `waterLevel`) to a unified dictionary structure.
- **Normalizer**: `normalizer.py` - Converts the transformed dictionaries into the strict `CanonicalRecord` Pydantic models defined in `canonical.py`.
- **Quality Validator**: `quality.py` - Performs deep data quality checks on canonical records (e.g., bounds checking, duplicate prevention, timestamp consistency).
- **Enricher**: `enricher.py` - Adds processing metadata and tracing tags to records that pass quality validation.
- **Canonical Model**: `canonical.py` - The absolute source of truth for data structures within the system boundary.
- **Pipeline Orchestrator**: `pipeline.py` - Manages the sequence of these steps and provides a unified `process()` interface.

## Lifecycle
`Raw DTO` -> `Schema Validation` -> `Transformation` -> `Normalization` -> `CanonicalRecord` -> `Quality Validation` -> `Enrichment` -> `Output`
