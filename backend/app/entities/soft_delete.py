"""Soft delete Mixins."""
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from app.persistence.types import DatabaseTypes
from app.entities.timestamps import get_utc_now

class SoftDeleteMixin:
    """Provides soft delete database flags and helper methods."""
    
    is_deleted: Mapped[bool] = mapped_column(
        DatabaseTypes.BOOLEAN, 
        default=False, 
        nullable=False,
        index=True,
        sort_order=920
    )
    
    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DatabaseTypes.DATETIME_UTC,
        nullable=True,
        sort_order=921
    )
    
    def soft_delete(self, user_id: Optional[str] = None) -> None:
        """Helper to mark entity as deleted and record timestamp."""
        self.is_deleted = True
        self.deleted_at = get_utc_now()
        
        # Integration with AuditMixin if present
        if hasattr(self, "deleted_by") and user_id is not None:
            setattr(self, "deleted_by", user_id)

    def restore(self) -> None:
        """Helper to restore a soft-deleted entity."""
        self.is_deleted = False
        self.deleted_at = None
        if hasattr(self, "deleted_by"):
            setattr(self, "deleted_by", None)
