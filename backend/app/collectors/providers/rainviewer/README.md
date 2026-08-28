# RainViewer Radar Collector

This module implements the RainViewer radar collection pipeline using the Flood Guardian `CollectorFoundation`.

## Architecture
- **Client**: Asynchronous HTTP client using `httpx` with timeout and retry logic. Fetches radar metadata from RainViewer's public API.
- **Parser**: Extracts raw data from RainViewer's JSON payload, separating past and nowcast frames.
- **Normalizer**: Converts parsed RainViewer frame data into Flood Guardian Canonical `NormalizedData` DTOs with spatial references.
- **Validator**: Ensures the structural integrity of the normalized data and prevents duplicate frame ingestion.
- **Mapper**: Prepares the DTO mapping for future Domain Entity or Radar Analysis Engine instantiation.
- **Health**: Provides availability and latency status for the RainViewer endpoint, ensuring radar frames are currently available.

## Lifecycle
`fetch()` -> `parse()` -> `normalize()` -> `validate()`
