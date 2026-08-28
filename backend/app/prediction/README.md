# Prediction Generation Pipeline

This module acts as the final translator of the Flood Decision Engine. It takes the raw, numerical `OrchestratorResult` and `FloodRiskAssessmentResult` and converts them into standardized, user-facing `FloodPredictionResult` objects. 

This output format is what will be consumed by the Notification Engine, REST APIs, and Mobile Apps.

## Architecture
- **Result (`result.py`)**: Defines `FloodPredictionResult` and `PredictionStatus` (`SAFE`, `WATCH`, `WARNING`, `DANGER`, `EMERGENCY`). This is the canonical output contract.
- **Classifier (`classifier.py`)**: Maps the internal 0-100 risk score into the public-facing `PredictionStatus`.
- **Builder (`builder.py`)**: Constructs the base prediction object, mapping IDs, extracting ETAs, and generating timestamps.
- **Explainer (`explainer.py`)**: Converts the technical `ReasonSummary` objects from the Risk Assessment into human-readable text explanations suitable for citizens.
- **Formatter (`formatter.py`)**: Extracts and prioritizes recommended actions. Ensures that if there are multiple recommendations, only the most critical one is highlighted as the primary action.
- **Validator (`validator.py`)**: A final safety check to ensure no malformed predictions (e.g. missing IDs, missing explanations) escape the backend.
- **Generator & Pipeline (`generator.py`, `pipeline.py`)**: Coordinates the sequential generation process.

## Data Flow
1. Receives `OrchestratorResult` containing all context and risk scores.
2. `PredictionBuilder` initializes `FloodPredictionResult`.
3. `PredictionClassifier` determines the Status (e.g. `WARNING`).
4. `PredictionExplainer` generates readable text based on risk factors.
5. `PredictionFormatter` sets the primary recommendation (e.g. `Move Valuable Items`).
6. `PredictionValidator` ensures structural integrity.
7. Return `FloodPredictionResult` to the upstream caller.
