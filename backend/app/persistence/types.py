"""Common database types and mappings."""
# Using SQLAlchemy 2.0 standard types
from sqlalchemy import String, Integer, Float, Boolean, DateTime, JSON, Enum, Numeric, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB

# Placeholders for future PostGIS integration
# from geoalchemy2 import Geometry, Geography

class DatabaseTypes:
    """Namespace for standardized database types across the application."""
    
    # UUIDs
    UUID = UUID(as_uuid=True)
    
    # JSON Types
    JSON_PG = JSONB
    JSON_GENERIC = JSON
    
    # Standard Strings
    STRING_SHORT = String(50)
    STRING_MEDIUM = String(255)
    STRING_LONG = String(1000)
    
    # Text types
    TEXT = Text
    LARGE_TEXT = Text
    
    # Numerics & Booleans
    BOOLEAN = Boolean
    DECIMAL = Numeric(precision=10, scale=2)
    
    # DateTimes
    DATETIME_UTC = DateTime(timezone=True)
    
    # Future Spatial
    # POINT = Geometry('POINT', srid=4326)
    # POLYGON = Geometry('POLYGON', srid=4326)
