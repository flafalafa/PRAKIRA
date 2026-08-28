"""Timestamp Mixins."""
from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column
from app.persistence.types import DatabaseTypes

def get_utc_now() -> datetime:
    """Return timezone-aware UTC current time."""
    return datetime.now(timezone.utc)

class TimestampMixin:
    """Provides created_at and updated_at timestamps automatically managed by SQLAlchemy."""
    
    created_at: Mapped[datetime] = mapped_column(
        DatabaseTypes.DATETIME_UTC,
        default=get_utc_now,
        nullable=False,
        sort_order=900
    )
    
    updated_at: Mapped[datetime] = mapped_column(
        DatabaseTypes.DATETIME_UTC,
        default=get_utc_now,
        onupdate=get_utc_now,
        nullable=False,
        sort_order=901
    )
