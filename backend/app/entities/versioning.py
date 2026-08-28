"""Optimistic Locking Mixins."""
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column, declared_attr

class VersioningMixin:
    """
    Provides a version counter for optimistic concurrency control.
    Protects against race conditions during simultaneous writes.
    """
    
    version: Mapped[int] = mapped_column(
        Integer, 
        default=1, 
        nullable=False,
        sort_order=930
    )
    
    @declared_attr
    def __mapper_args__(cls):
        """Instructs SQLAlchemy to use this column for optimistic locking."""
        return {"version_id_col": cls.version}
