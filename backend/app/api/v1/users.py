"""Users routes: me, update profile."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.permissions import get_current_user
from app.db.session import get_db
from app.db.models.user import User
from app.schemas.user import UserResponse, UserUpdate
from app.services.user_service import get_user_by_id

router = APIRouter()


def user_to_response(user: User) -> UserResponse:
    return UserResponse(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        is_active=user.is_active,
        email_verified=user.email_verified,
        created_at=user.created_at,
        role_names=[r.name for r in (user.roles or [])],
    )


@router.get("/me", response_model=UserResponse)
async def get_me(
    current_user: User = Depends(get_current_user),
):
    """Current user profile."""
    return user_to_response(current_user)


@router.patch("/me", response_model=UserResponse)
async def update_me(
    data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update current user profile."""
    if data.full_name is not None:
        current_user.full_name = data.full_name
    await db.flush()
    await db.refresh(current_user)
    return user_to_response(current_user)
