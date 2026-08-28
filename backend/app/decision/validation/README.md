# Enterprise Decision Engine Validation

This module is the testbed and quality assurance (QA) framework for the entire Flood Decision Engine. It ensures that the complex orchestration of Weather, Hydrology, Radar, Risk, and Prediction engines behaves deterministically and correctly under various disaster scenarios.

## Architecture
- **Scenario (`scenario.py`)**: Defines `ValidationScenario`, which acts as a mocked environment (e.g., "Heavy Rain + High River") with an expected outcome (e.g., `EMERGENCY`).
- **Registry (`registry.py`)**: Stores and manages all predefined test scenarios.
- **Simulator (`simulator.py`)**: A runner that executes a single scenario through the entire `DecisionOrchestrator` and `PredictionPipeline` from start to finish.
- **Consistency (`consistency.py`)**: Validates the logical soundness of a prediction (e.g., if Risk Score > 90, Status *must* be `EMERGENCY`. If not, the engine is inconsistent).
- **Validator (`validator.py`)**: Compares the simulated outcome against the scenario's expected outcome.
- **Metrics & Report (`metrics.py`, `report.py`)**: Aggregates execution time, success rate, and consistency scores into a final validation report.
- **Runner (`runner.py`)**: The main entry point to execute the full suite of validation scenarios.

## Execution Flow
1. Load all predefined scenarios from `ScenarioRegistry`.
2. For each scenario:
   a. Inject mocked `OrchestratorContext` into the `SimulationRunner`.
   b. Execute the full Decision Orchestrator pipeline.
   c. Execute the Prediction Pipeline.
   d. `ScenarioValidator` checks if the output matches expectations.
   e. `ConsistencyValidator` checks if the output is logically sound.
3. Generate and return a `ValidationReport` with metrics.
