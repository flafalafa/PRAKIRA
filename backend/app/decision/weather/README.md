# Weather Analysis Engine

This module evaluates meteorological conditions using Canonical Weather and Rainfall data.

## Architecture
- **Context (`context.py`)**: `WeatherContext` holding normalized weather and rainfall data.
- **Metrics (`metrics.py`)**: Computes statistical summaries (e.g., average rainfall, total accumulation, data completeness).
- **Rules (`rules.py`)**: Pluggable analysis rules (e.g., `HeavyRainRule`) that trigger based on specific thresholds.
- **Policy (`policy.py`)**: Applies confidence penalties or severity overrides based on completeness or extreme conditions.
- **Result (`result.py`)**: `WeatherAnalysisResult` combining all metrics, triggered rules, and explanations.
- **Analyzer & Engine (`analyzer.py`, `engine.py`)**: Orchestrates the analysis flow.

## Analysis Flow
1. Load `WeatherContext`.
2. Compute `WeatherMetrics`.
3. `WeatherAnalyzer` evaluates all registered rules.
4. Construct initial `WeatherAnalysisResult`.
5. `WeatherPolicyEngine` adjusts confidence and severity.
6. Return `WeatherAnalysisResult`.
