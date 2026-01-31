"""User CRUD and auth-related logic; calls email on signup/reset."""
import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.auth import hash_password
from app.core.security import create_reset_token
from app.core.email_service import send_signup_confirmation, send_reset_password_email
from app.db.models.user import User
from app.db.models.role import Role
from app.db.models.role import UserRole
from app.schemas.user import UserCreate


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def get_user_by_id(db: AsyncSession, user_id: uuid.UUID) -> User | None:
    result = await db.execute(
        select(User).where(User.id == user_id).options(selectinload(User.roles))
    )
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, data: UserCreate) -> User:
    user = User(
        id=uuid.uuid4(),
        email=data.email,
        hashed_password=hash_password(data.password),
        full_name=data.full_name,
        is_active=True,
        email_verified=False,
    )
    db.add(user)
    await db.flush()

    # Assign default role "user"
    role_result = await db.execute(select(Role).where(Role.name == "user"))
    role = role_result.scalar_one_or_none()
    if role:
        user_role = UserRole(user_id=user.id, role_id=role.id)
        db.add(user_role)
    await db.flush()
    result = await db.execute(select(User).where(User.id == user.id).options(selectinload(User.roles)))
    user = result.scalar_one()
    # Send welcome email (non-blocking best effort)
    try:
        await send_signup_confirmation(user.email, user.full_name or user.email)
    except Exception:
        pass
    return user


async def set_reset_password_token(db: AsyncSession, user: User) -> str:
    from app.config import get_settings
    settings = get_settings()
    token = create_reset_token(user.id)
    user.reset_password_token = token
    user.reset_password_expires = datetime.now(timezone.utc) + timedelta(minutes=settings.RESET_PASSWORD_EXPIRE_MINUTES)
    await db.flush()
    try:
        await send_reset_password_email(user.email, token)
    except Exception:
        pass
    return token


async def reset_password(db: AsyncSession, user_id: uuid.UUID, new_password: str) -> User | None:
    """Update user password and clear reset token."""
    user = await get_user_by_id(db, user_id)
    if not user:
        return None
    user.hashed_password = hash_password(new_password)
    user.reset_password_token = None
    user.reset_password_expires = None
    await db.flush()
    await db.refresh(user)
    return user
