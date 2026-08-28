"""Request Context management."""
from contextvars import ContextVar
from typing import Any

_request_context_ctx_var: ContextVar[dict[str, Any]] = ContextVar("request_context", default={})

def get_request_context() -> dict[str, Any]:
    """Get the current request context."""
    return _request_context_ctx_var.get().copy()

def set_request_context(**kwargs: Any) -> None:
    """Set request context variables."""
    ctx = _request_context_ctx_var.get().copy()
    ctx.update(kwargs)
    _request_context_ctx_var.set(ctx)

def clear_request_context() -> None:
    """Clear request context."""
    _request_context_ctx_var.set({})
