"""API v1: aggregate all sub-routers."""
from fastapi import APIRouter

from app.api.v1 import auth, users, subscriptions, webhooks, storage
from app.api.v1.admin import users as admin_users, roles as admin_roles

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(subscriptions.router, prefix="/subscriptions", tags=["subscriptions"])
api_router.include_router(webhooks.router, prefix="/webhooks", tags=["webhooks"])
api_router.include_router(storage.router, prefix="/storage", tags=["storage"])
api_router.include_router(admin_users.router, prefix="/admin/users", tags=["admin-users"])
api_router.include_router(admin_roles.router, prefix="/admin/roles", tags=["admin-roles"])
