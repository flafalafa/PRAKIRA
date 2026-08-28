# Hydrology Analysis Engine

This module evaluates river conditions using Canonical River observations.

## Architecture
- **Context (`context.py`)**: `HydrologyContext` holding normalized river data and metadata (like max capacity).
- **Metrics (`metrics.py`)**: Computes statistical summaries (e.g., rise rate, capacity usage percentage).
- **Rules (`rules.py`)**: Pluggable analysis rules (e.g., `RapidWaterRiseRule`, `HighCapacityUsageRule`).
- **Policy (`policy.py`)**: Applies confidence penalties or critical overrides based on overflow or missing data.
- **Result (`result.py`)**: `HydrologyAnalysisResult` combining all metrics, status, and explanations.
- **Analyzer & Engine (`analyzer.py`, `engine.py`)**: Orchestrates the hydrology analysis flow.

## Analysis Flow
1. Load `HydrologyContext`.
2. Compute `HydrologyMetrics`.
3. `HydrologyAnalyzer` evaluates all registered rules.
4. Construct initial `HydrologyAnalysisResult` (determines River Status).
5. `HydrologyPolicyEngine` adjusts confidence and severity.
6. Return `HydrologyAnalysisResult`.
