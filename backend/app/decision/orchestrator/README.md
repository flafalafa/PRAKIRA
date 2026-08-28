# Enterprise Decision Orchestrator

This module serves as the central conductor for the Flood Decision Engine, coordinating the execution of all specialized analysis engines (Weather, Hydrology, Radar, Risk).

## Architecture
- **Context (`context.py`)**: `OrchestratorContext` holding raw observation data before it is routed to specific engines.
- **Registry (`registry.py`)**: `EngineRegistry` maintains a list of available analysis engines and their execution priority. Engines are registered here dynamically.
- **Executor (`executor.py`)**: Safely invokes any registered engine and catches execution failures without crashing the whole system.
- **Pipeline (`pipeline.py`)**: Wraps the raw context into engine-specific contexts (e.g., `WeatherContext`, `HydrologyContext`) before executing them.
- **Workflow (`workflow.py`)**: Defines the logical flow of execution. Runs base engines first, collects their results, and feeds them into the Risk Assessment engine.
- **State (`state.py`)**: Tracks the workflow lifecycle (`RUNNING`, `SUCCESS`, `PARTIAL_SUCCESS`, `FAILED`).
- **Result (`result.py`)**: `OrchestratorResult` encapsulates the final outputs of all executed engines, along with metadata and error logs.
- **Orchestrator (`orchestrator.py`)**: The main entry point (`DecisionOrchestrator.process()`) that triggers the workflow.

## Execution Flow
1. Load `OrchestratorContext`.
2. Look up enabled engines in `EngineRegistry`.
3. `WorkflowPipeline` executes enabled base engines (Weather, Hydrology, Radar).
4. Partial failures are caught; if Weather fails, Hydrology still runs.
5. Base engine results are collected into a `RiskContext`.
6. `FloodRiskAssessmentEngine` is executed.
7. Final `OrchestratorResult` is generated and returned, marking state as `SUCCESS` or `PARTIAL_SUCCESS`.
