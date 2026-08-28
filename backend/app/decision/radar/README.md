# Radar Motion Analysis Engine

This module evaluates the spatial movement and intensity of storm cells using Canonical Radar observations.

## Architecture
- **Context (`context.py`)**: `RadarContext` holding sequences of radar frames.
- **Motion & Tracking (`motion.py`, `tracker.py`)**: Analyzes frame-to-frame changes to identify storm cells and extract their movement vectors (speed and direction).
- **Trajectory & ETA (`trajectory.py`, `eta.py`)**: Projects the path of storm cells to determine if they intersect the monitored area and calculates Estimated Time of Arrival (ETA).
- **Metrics (`metrics.py`)**: Computes radar coverage and data completeness.
- **Rules (`rules.py`)**: Pluggable rules (e.g., `StormApproachingRule`, `RapidCellGrowthRule`).
- **Policy (`policy.py`)**: Adjusts confidence for missing frames or elevates severity for imminent storm arrivals.
- **Result (`result.py`)**: `RadarAnalysisResult` aggregating ETA, direction, speed, and severity.
- **Analyzer & Engine (`analyzer.py`, `engine.py`)**: Orchestrates the radar analysis pipeline.

## Analysis Flow
1. Load `RadarContext` containing multiple frames.
2. Check frame completeness in `RadarMetrics`.
3. Extract vectors in `MotionCalculator`.
4. Identify cells in `CellTracker`.
5. Project paths in `TrajectoryEstimator`.
6. Calculate `ETA` for approaching cells.
7. `RadarAnalyzer` evaluates all rules against this data.
8. Construct initial `RadarAnalysisResult`.
9. `RadarPolicyEngine` applies final adjustments.
10. Return `RadarAnalysisResult`.
