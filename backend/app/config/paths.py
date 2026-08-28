"""Centralized filesystem paths."""
from pathlib import Path

# Resolves to PRAKIRA/backend
ROOT_DIR = Path(__file__).resolve().parent.parent.parent

# Core application directories
APP_DIR = ROOT_DIR / "app"
DATA_DIR = ROOT_DIR / "data"
LOG_DIR = ROOT_DIR / "logs"
TEMP_DIR = DATA_DIR / "temp"
UPLOAD_DIR = DATA_DIR / "uploads"

def ensure_directories() -> None:
    """Ensure all required directories exist."""
    directories = [DATA_DIR, LOG_DIR, TEMP_DIR, UPLOAD_DIR]
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
