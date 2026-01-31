"""Admin: list roles."""
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.permissions import get_current_user, require_role
from app.db.session import get_db
from app.db.models.user import User
from app.db.models.role import Role
from app.schemas.role import RoleResponse

router = APIRouter()


@router.get("", response_model=list[RoleResponse])
async def list_roles(
    current_user: User = Depends(require_role("admin")),
    db: AsyncSession = Depends(get_db),
):
    """List all roles (admin)."""
    result = await db.execute(select(Role).order_by(Role.name))
    roles = result.scalars().all()
    return [RoleResponse(id=r.id, name=r.name, description=r.description) for r in roles]
