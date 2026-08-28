# Enterprise Collector Integration & Validation

This module validates that all individual Data Collectors successfully integrate with the Flood Guardian Enterprise Normalization Pipeline and Scheduler.

## Architecture
- **Contracts (`contracts.py`)**: Strict Python `Protocols` defining the interface every Collector must implement (`connect`, `fetch`, `parse`, `normalize`, `validate`, `health`, `metadata`, `disconnect`).
- **Validator (`validator.py`)**: The execution engine that runs runtime checks against registered collector instances.
- **Health (`health.py`)**: Probes the `health()` endpoints of every collector in the ecosystem.
- **Diagnostics (`diagnostics.py`)**: Aggregates component states into a unified system state dump.
- **Orchestrator (`integration.py`)**: Orchestrates the verification suite and produces a final `ReadinessReport`.

## Integration Validation Lifecycle
1. Retrieve registered components from `IntegrationRegistry`.
2. Perform structural checks against `CollectorContract`.
3. Check dynamic health using `IntegrationHealth`.
4. Compile diagnostics and compute a final `ReadinessStatus` (READY, PARTIALLY_READY, NOT_READY).
