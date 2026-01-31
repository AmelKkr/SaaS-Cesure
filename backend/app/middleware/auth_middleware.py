"""Auth middleware: inject current_user from JWT is done via Depends(get_current_user) in routes.
No global middleware needed; FastAPI dependencies handle per-route auth."""
# This module is kept for documentation; actual auth is in core/permissions.py
