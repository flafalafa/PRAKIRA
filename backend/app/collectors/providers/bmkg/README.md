# BMKG Weather Collector

This module implements the BMKG data collection pipeline using the Flood Guardian `CollectorFoundation`.

## Architecture
- **Client**: Asynchronous HTTP client using `httpx` with timeout and retry logic.
- **Parser**: Extracts raw data from BMKG's Open Data XML format.
- **Normalizer**: Converts parsed BMKG parameters into Flood Guardian Canonical `NormalizedData` DTOs.
- **Validator**: Ensures the structural integrity of the normalized data.
- **Mapper**: Prepares the DTO mapping for future Domain Entity instantiation.
- **Health**: Provides availability and latency status for the BMKG endpoint.

## Lifecycle
`fetch()` -> `parse()` -> `normalize()` -> `validate()`
