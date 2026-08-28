# OpenWeather Collector

This module implements the OpenWeather data collection pipeline using the Flood Guardian `CollectorFoundation`.

## Architecture
- **Client**: Asynchronous HTTP client using `httpx` with timeout, retry, and exponential backoff logic. Requires an API Key for authentication.
- **Parser**: Extracts raw data from OpenWeather's JSON payload (specifically optimized for the OneCall API).
- **Normalizer**: Converts parsed OpenWeather parameters into Flood Guardian Canonical `NormalizedData` DTOs.
- **Validator**: Ensures the structural integrity of the normalized data.
- **Mapper**: Prepares the DTO mapping for future Domain Entity instantiation.
- **Health**: Provides availability, latency status, and authentication validation for the OpenWeather endpoint.

## Lifecycle
`fetch()` -> `parse()` -> `normalize()` -> `validate()`
