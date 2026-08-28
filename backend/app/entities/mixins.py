"""Common aggregation of entity mixins."""
from app.entities.timestamps import TimestampMixin
from app.entities.audit import AuditMixin
from app.entities.soft_delete import SoftDeleteMixin
from app.entities.versioning import VersioningMixin

class StandardEntityMixin(
    TimestampMixin,
    VersioningMixin
):
    """
    A convenient mixin combining standard capabilities:
    - created_at, updated_at
    - version (optimistic locking)
    """
    pass

class FullAuditEntityMixin(
    StandardEntityMixin,
    AuditMixin,
    SoftDeleteMixin
):
    """
    Combines all mixins for highly audited entities (e.g., Reports, Users).
    - created_at, updated_at
    - version
    - created_by, updated_by, deleted_by
    - is_deleted, deleted_at
    """
    pass
