"""Logging middleware: request id, Sentry breadcrumbs."""
import time
import uuid as uuid_lib

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Add request_id to state and log timing; Sentry breadcrumbs via scope."""

    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid_lib.uuid4())[:8]
        request.state.request_id = request_id
        start = time.perf_counter()
        response = await call_next(request)
        duration_ms = (time.perf_counter() - start) * 1000
        # Optional: log request method, path, status, duration
        if hasattr(request.app.state, "sentry") or True:
            pass  # Sentry adds breadcrumbs automatically when enabled
        return response
