# Enterprise Scheduler & Collector Orchestrator

This module implements the execution and orchestration engine for all Flood Guardian data collectors.

## Architecture
- **Job Registry**: An in-memory registry (`registry.py`) that holds the definitions (`Job`) of tasks to be executed. Each collector pipeline is registered here as a Job.
- **Dispatcher**: The trigger mechanism (`dispatcher.py`) that looks up a job in the registry and initiates execution.
- **Executor**: The core runner (`executor.py`) that wraps every job execution with safety nets: Timeouts and Retry Policies (Exponential Backoff). It tracks the `ExecutionContext`.
- **Orchestrator**: The macro-coordinator (`orchestrator.py`) responsible for the specific business logic of data collection order (BMKG -> OpenWeather -> RainViewer -> River).
- **Scheduler**: The long-running daemon (`scheduler.py`) that triggers the orchestrator on a specific interval (tick).

## Lifecycle
`Scheduler Loop` -> `Orchestrator` -> `Dispatcher` -> `Registry Lookup` -> `Executor` -> `Job Function`
