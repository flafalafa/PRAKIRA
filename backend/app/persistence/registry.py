"""Central ORM registry for future model registration."""

# Central import point for all ORM models.
# This ensures that Base.metadata.create_all() (or Alembic) 
# sees all models before generating migrations.

# Future imports will look like:
# from app.models.weather import WeatherData
# from app.models.prediction import FloodPrediction

from app.core.logger import get_logger

logger = get_logger(__name__)

def register_models() -> None:
    """
    Called by the bootstrap process or Alembic env.py to ensure 
    all declarative models are loaded into the SQLAlchemy registry.
    """
    logger.info("ORM registry initialized. Models loaded into metadata.")
    from app.persistence.models.prediction import FloodPredictionModel
