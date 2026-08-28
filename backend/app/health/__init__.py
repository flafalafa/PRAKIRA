import datetime
from datetime import timezone

# Global application start time initialized on module import
APP_START_TIME = datetime.datetime.now(timezone.utc)

def get_uptime_string() -> str:
    """Calculate and return application uptime as a formatted string."""
    now = datetime.datetime.now(timezone.utc)
    delta = now - APP_START_TIME
    days = delta.days
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{days}d {hours}h {minutes}m {seconds}s"
