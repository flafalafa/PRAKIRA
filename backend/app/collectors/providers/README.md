# Collector Providers

This directory is the home for all external data integrations (e.g. BMKG, OpenWeather, internal IoT sensors).

## Rules
1. Never bypass the `CollectorPipeline`.
2. Inherit from `BaseCollector`.
3. Register your provider in the `CollectorRegistry`.
4. Ensure outputs are mapped strictly to `NormalizedData` DTOs.
