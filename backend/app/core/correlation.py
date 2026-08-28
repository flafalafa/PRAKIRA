"""Correlation ID management using ContextVars."""
import uuid
from contextvars import ContextVar

_correlation_id_ctx_var: ContextVar[str] = ContextVar("correlation_id", default="")

def get_correlation_id() -> str:
    """Get the current correlation ID."""
    return _correlation_id_ctx_var.get()

def set_correlation_id(correlation_id: str | None = None) -> str:
    """Set the correlation ID for the current context."""
    if not correlation_id:
        correlation_id = str(uuid.uuid4())
    _correlation_id_ctx_var.set(correlation_id)
    return correlation_id
