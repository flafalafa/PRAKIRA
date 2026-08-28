# Flood Decision Engine Foundation

This module forms the foundation of the Enterprise Flood Decision Engine, the core analytical component of the Flood Guardian platform.

## Architecture
- **Context (`context.py`)**: Defines `DecisionContext`, an immutable snapshot of all normalized data points required for a single evaluation run.
- **State (`state.py`)**: Defines `EngineState`, a mutable tracker that holds the current execution status, missing data logs, and intermediate rule evidence.
- **Rules & Registry (`rules.py`, `registry.py`)**: Pluggable interface for analysis rules.
- **Executor (`executor.py`)**: Evaluates all registered rules against the context safely.
- **Policy (`policy.py`)**: Applies overarching business policies (e.g., confidence penalties) to intermediate rule results.
- **Result & Explanation (`result.py`, `explanation.py`)**: Transparent output format guaranteeing every decision provides its reasoning, triggered rules, and confidence levels.
- **Engine (`engine.py`)**: The main orchestrator connecting the components together.

## Execution Flow
1. Load & Validate `DecisionContext`.
2. `RuleExecutor` runs all registered rules against the context.
3. Intermediate `DecisionResult` is formed.
4. `PolicyEngine` applies business logic to finalize the result.
5. `DecisionExplanation` is generated for transparency.
6. Final `DecisionResult` is returned.
