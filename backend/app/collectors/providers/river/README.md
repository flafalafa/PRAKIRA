# River Hydrology Collector

This module implements the River Hydrology data collection pipeline using the Flood Guardian `CollectorFoundation`.

## Architecture
- **Multi-Provider Client**: A robust asynchronous HTTP client (`httpx`) designed to iterate and fetch river telemetry (Water Level, Flow Rate) from multiple configured sources (e.g., BBWS, BPBD, IoT sensors). Features timeout, retry, and exponential backoff mechanisms.
- **Parser**: Translates raw payload strings into unified `RiverParsedData` and `StationData` objects regardless of the underlying JSON structure.
- **Normalizer**: Standardizes disparate provider metrics into the canonical Flood Guardian `NormalizedData` format. Converts all timestamps to UTC and standardizes spatial coordinates.
- **Validator**: Ensures data integrity by rejecting null, negative, or duplicate observations (water levels, flow rates) before they enter the system.
- **Mapper**: Prepares the DTO mapping for future `River` Aggregate instantiation inside the Domain layer.
- **Health**: Provides ping tests for all configured telemetry providers, reporting degraded status if any specific provider goes offline.

## Lifecycle
`fetch(provider)` -> `parse()` -> `normalize()` -> `validate()`
