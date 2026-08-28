# Enterprise Flood Risk Assessment Engine

This engine combines the outputs of the Weather, Hydrology, and Radar Analysis engines into a unified, actionable Flood Risk Assessment.

## Architecture
- **Context (`context.py`)**: `RiskContext` aggregates the results of all sub-engines (`WeatherAnalysisResult`, `HydrologyAnalysisResult`, `RadarAnalysisResult`).
- **Aggregator (`aggregator.py`)**: Extracts and flattens key risk factors (e.g., rainfall intensity, capacity usage, storm ETA) into a single map.
- **Scoring (`scoring.py`)**: Converts raw factors into 0-100 scores and computes the final weighted overall risk score.
- **Weighting (`weighting.py`)**: Configurable weight distribution (e.g., Hydrology 40%, Weather 30%, Radar 20%, Historical 10%). Supports dynamic re-normalization if data is missing.
- **Metrics (`metrics.py`)**: Averages the confidence scores of the underlying analyses.
- **Rules (`rules.py`)**: Evaluates compound risks (e.g., `CompoundRiskRule`) and generates human-readable recommendations (e.g., "Prepare Evacuation").
- **Policy (`policy.py`)**: Classifies the numerical score into a `RiskLevel` (e.g., `VERY_LOW`, `EXTREME`).
- **Result (`result.py`)**: The final `FloodRiskAssessmentResult` containing scores, recommendations, and deep explanations.
- **Calculator & Engine (`calculator.py`, `engine.py`)**: Orchestrates the entire risk synthesis process.

## Analysis Flow
1. Load `RiskContext` with all available sub-engine results.
2. `RiskAggregator` flattens data into a `factors` dictionary.
3. `ScoringEngine` calculates sub-scores and the final `overall_score` based on `WeightConfig`.
4. `RiskMetrics` calculates the overall confidence level.
5. `RiskRuleRegistry` evaluates rules to generate `recommendations` based on the factors.
6. Build initial `FloodRiskAssessmentResult`.
7. Extract contribution explanations (why the score is what it is).
8. `RiskPolicyEngine` maps the 0-100 score to a categorical `RiskLevel`.
9. Return the final unified assessment.
