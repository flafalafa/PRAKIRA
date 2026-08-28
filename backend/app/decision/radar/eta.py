"""Estimated Time of Arrival (ETA) Calculation."""
from typing import Dict, Any, Optional

class ETACalculator:
    @staticmethod
    def calculate_eta(trajectory_data: Dict[str, Any], motion_data: Dict[str, Any]) -> Optional[int]:
        """Calculates ETA in minutes based on distance and speed."""
        if not trajectory_data.get("path_intersects_target"):
            return None
            
        distance = trajectory_data.get("distance_to_target_km", 0.0)
        speed = motion_data.get("avg_speed", 0.0)
        
        if speed <= 0:
            return None
            
        hours = distance / speed
        return int(hours * 60)
