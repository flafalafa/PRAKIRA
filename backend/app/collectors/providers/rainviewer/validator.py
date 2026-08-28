"""Validates the Canonical NormalizedData DTO for RainViewer."""
from app.collectors.dto.normalized import NormalizedData
from app.core.logger import get_logger

logger = get_logger(__name__)

class RainViewerValidator:
    @staticmethod
    def validate(normalized_data: NormalizedData) -> bool:
        if not normalized_data.time_series:
            logger.warning("RainViewer Validation Failed: No radar frames found.")
            return False
            
        # Track seen timestamps to check for duplicates
        seen_frames = set()
        for item in normalized_data.time_series:
            if not item.get("timestamp") or not item.get("value"):
                logger.warning(f"RainViewer Validation Failed: Missing fields in frame: {item}")
                return False
                
            frame_id = f"{item['parameter']}_{item['timestamp'].timestamp()}"
            if frame_id in seen_frames:
                logger.warning(f"RainViewer Validation Failed: Duplicate frame found: {frame_id}")
                return False
            seen_frames.add(frame_id)
                
        return True
