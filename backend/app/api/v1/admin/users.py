"""Admin: list users, assign role."""
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.permissions import get_current_user, require_role
from app.db.session import get_db
from app.db.models.user import User
from app.db.models.role import Role
from app.db.models.role import UserRole
from app.schemas.user import UserResponse

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


@router.get("", response_model=list[UserResponse])
async def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(require_role("admin")),
    db: AsyncSession = Depends(get_db),
):
    """List users (admin)."""
    result = await db.execute(
        select(User)
        .options(selectinload(User.roles))
        .order_by(User.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    users = result.scalars().all()
    return [user_to_response(u) for u in users]


@router.patch("/{user_id}/role")
async def assign_role(
    user_id: UUID,
    role_name: str = Query(..., description="Role name to assign"),
    current_user: User = Depends(require_role("admin")),
    db: AsyncSession = Depends(get_db),
):
    """Assign a role to a user (admin)."""
    role_result = await db.execute(select(Role).where(Role.name == role_name))
    role = role_result.scalar_one_or_none()
    if not role:
        raise HTTPException(status_code=404, detail=f"Role '{role_name}' not found")
    user_result = await db.execute(select(User).where(User.id == user_id).options(selectinload(User.roles)))
    user = user_result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await db.execute(delete(UserRole).where(UserRole.user_id == user_id))
    db.add(UserRole(user_id=user_id, role_id=role.id))
    await db.flush()
    result = await db.execute(select(User).where(User.id == user_id).options(selectinload(User.roles)))
    user = result.scalar_one()
    return {"message": f"Role '{role_name}' assigned", "user": user_to_response(user)}
