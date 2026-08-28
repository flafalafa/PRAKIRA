"""Central SQLAlchemy metadata."""
from sqlalchemy import MetaData
from app.persistence.naming import NAMING_CONVENTION

# Centralized metadata for Alembic migrations and Declarative Base.
# Applying naming conventions here ensures all auto-generated schemas 
# (like foreign keys) have predictable, database-agnostic names.
metadata = MetaData(naming_convention=NAMING_CONVENTION)
