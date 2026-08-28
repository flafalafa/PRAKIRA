"""Audit Mixins for tracking user actions."""
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from app.persistence.types import DatabaseTypes

class AuditMixin:
    """Provides placeholders for audit trailing (who created/updated/deleted)."""
    
    # Placeholders for future authentication integration.
    # Typically these will store user UUIDs or system service names.
    created_by: Mapped[Optional[str]] = mapped_column(
        DatabaseTypes.STRING_MEDIUM, 
        nullable=True,
        sort_order=910
    )
    
    updated_by: Mapped[Optional[str]] = mapped_column(
        DatabaseTypes.STRING_MEDIUM, 
        nullable=True,
        sort_order=911
    )
    
    deleted_by: Mapped[Optional[str]] = mapped_column(
        DatabaseTypes.STRING_MEDIUM, 
        nullable=True,
        sort_order=912
    )
