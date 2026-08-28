"""Enterprise structured JSON logger."""
import logging
import json
from datetime import datetime, timezone
from typing import Any

from app.config.settings import settings
from app.core.correlation import get_correlation_id
from app.core.request_context import get_request_context

SENSITIVE_KEYS = {"password", "token", "secret", "api_key", "authorization"}

class EnterpriseJSONFormatter(logging.Formatter):
    """Custom formatter to output enterprise-grade JSON logs."""
    
    def _mask_sensitive_data(self, data: dict[str, Any]) -> dict[str, Any]:
        safe_data = data.copy()
        for k, v in safe_data.items():
            if any(sensitive in k.lower() for sensitive in SENSITIVE_KEYS):
                safe_data[k] = "****"
            elif isinstance(v, dict):
                safe_data[k] = self._mask_sensitive_data(v)
        return safe_data

    def format(self, record: logging.LogRecord) -> str:
        log_obj: dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "environment": settings.app.environment.value,
            "correlation_id": get_correlation_id(),
        }
        
        # Merge request context
        log_obj.update(get_request_context())

        if record.exc_info:
            log_obj["exception_type"] = record.exc_info[0].__name__ if record.exc_info[0] else None
            log_obj["stack_trace"] = self.formatException(record.exc_info)
            
        # Add extra attributes
        extra_attrs = {}
        for key, value in record.__dict__.items():
            if key not in ["args", "asctime", "created", "exc_info", "exc_text", 
                           "filename", "funcName", "levelname", "levelno", "lineno", 
                           "module", "msecs", "message", "msg", "name", "pathname", 
                           "process", "processName", "relativeCreated", "stack_info", "thread", "threadName"]:
                if key != "color_message":
                    extra_attrs[key] = value
                    
        if extra_attrs:
            log_obj["extra"] = self._mask_sensitive_data(extra_attrs)

        return json.dumps(log_obj)

def get_logger(name: str) -> logging.Logger:
    """Get a structured logger."""
    return logging.getLogger(name)
