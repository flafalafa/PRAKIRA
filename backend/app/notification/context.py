"""Notification Context."""
from dataclasses import dataclass, field
from typing import Dict, Any
from app.prediction.result import FloodPredictionResult

@dataclass
class NotificationContext:
    prediction: FloodPredictionResult
    area_metadata: Dict[str, Any] = field(default_factory=dict)
    prediction_metadata: Dict[str, Any] = field(default_factory=dict)
    execution_metadata: Dict[str, Any] = field(default_factory=dict)
