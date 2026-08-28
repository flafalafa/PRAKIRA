"""Identity Mixins."""
import uuid
from sqlalchemy.orm import Mapped, mapped_column
from app.persistence.types import DatabaseTypes

class UUIDIdentifierMixin:
    """Provides a standard UUID primary key for an entity."""
    
    id: Mapped[uuid.UUID] = mapped_column(
        DatabaseTypes.UUID,
        primary_key=True,
        default=uuid.uuid4,
        index=True,
        sort_order=-100  # Ensures ID is typically the first column
    )
