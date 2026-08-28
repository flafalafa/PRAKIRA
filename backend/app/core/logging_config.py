"""Logging configuration and setup."""
import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

from app.config.settings import settings
from app.core.logger import EnterpriseJSONFormatter

def setup_enterprise_logging() -> None:
    """Initialize structured enterprise logging."""
    root_logger = logging.getLogger()
    
    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
        
    log_level = getattr(logging, settings.logging.level.upper(), logging.INFO)
    root_logger.setLevel(log_level)
    
    formatter = EnterpriseJSONFormatter()
    
    if settings.logging.log_to_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)
        
    if settings.logging.log_to_file:
        log_path = Path(settings.logging.log_file_path)
        # Ensure log directory exists, resolving relative to project root
        log_dir = Path(__file__).resolve().parent.parent.parent.parent / log_path.parent
        log_dir.mkdir(parents=True, exist_ok=True)
        
        full_log_path = Path(__file__).resolve().parent.parent.parent.parent / log_path
        file_handler = RotatingFileHandler(
            filename=full_log_path,
            maxBytes=10 * 1024 * 1024,  # 10 MB
            backupCount=5,
            encoding="utf-8"
        )
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    
    # Ensure third-party loggers use this configuration
    logging.getLogger("uvicorn.access").handlers = root_logger.handlers
    logging.getLogger("uvicorn.error").handlers = root_logger.handlers
    logging.getLogger("fastapi").handlers = root_logger.handlers
