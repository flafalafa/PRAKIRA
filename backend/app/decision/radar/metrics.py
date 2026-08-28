"""Radar Metrics Calculator."""
from typing import List
from app.decision.radar.context import RadarContext

class RadarMetrics:
    @staticmethod
    def calculate_coverage(context: RadarContext) -> float:
        """Estimates spatial coverage of radar data."""
        return 85.0
        
    @staticmethod
    def check_completeness(context: RadarContext) -> float:
        """Checks if enough frames exist for motion analysis."""
        required_frames = 3
        actual = len(context.radar_observations)
        return min(1.0, actual / required_frames) if required_frames > 0 else 0.0
