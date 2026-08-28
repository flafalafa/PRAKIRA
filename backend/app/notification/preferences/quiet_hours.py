"""Quiet Hours Evaluator."""
from datetime import datetime
import pytz
from app.notification.preferences.profile import QuietHoursConfig
from app.core.logger import get_logger

logger = get_logger(__name__)

class QuietHoursEvaluator:
    @staticmethod
    def is_active(config: QuietHoursConfig, current_time: datetime = None) -> bool:
        if not config.enabled:
            return False
            
        if current_time is None:
            current_time = datetime.now(pytz.utc)
            
        tz = pytz.timezone(config.timezone)
        local_time = current_time.astimezone(tz).time()
        
        start = config.start_time
        end = config.end_time
        
        if start < end:
            return start <= local_time <= end
        else:
            return local_time >= start or local_time <= end
