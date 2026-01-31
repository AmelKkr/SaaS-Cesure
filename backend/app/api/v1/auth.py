"""Auth routes: signup, login, refresh, forgot-password, reset-password."""
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.core.auth import (
    authenticate_user,
    get_tokens_for_user,
    verify_refresh_token,
    verify_reset_token,
)
from app.db.session import get_db
from app.schemas.auth import (
    LoginRequest,
    SignupRequest,
    TokenResponse,
    RefreshRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
)
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import (
    create_user,
    get_user_by_email,
    get_user_by_id,
    reset_password,
    set_reset_password_token,
)

router = APIRouter()


def user_to_response(user) -> UserResponse:
    return UserResponse(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        is_active=user.is_active,
        email_verified=user.email_verified,
        created_at=user.created_at,
        role_names=[r.name for r in (user.roles or [])],
    )


@router.post("/signup", response_model=dict)
async def signup(
    data: SignupRequest,
    db: AsyncSession = Depends(get_db),
):
    """Register new user; returns tokens and user."""
    existing = await get_user_by_email(db, data.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    user = await create_user(db, UserCreate(email=data.email, password=data.password, full_name=data.full_name))
    tokens = get_tokens_for_user(str(user.id))
    return {"user": user_to_response(user), **tokens}


@router.post("/login", response_model=dict)
async def login(
    data: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    """Login; returns tokens and user."""
    user = await get_user_by_email(db, data.email)
    if not user or not authenticate_user(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account disabled")
    user_with_roles = await get_user_by_id(db, user.id)
    if user_with_roles:
        user = user_with_roles
    tokens = get_tokens_for_user(str(user.id))
    return {"user": user_to_response(user), **tokens}


@router.post("/refresh", response_model=TokenResponse)
async def refresh(
    data: RefreshRequest,
    db: AsyncSession = Depends(get_db),
):
    """Issue new access token from refresh token."""
    user_id_str = verify_refresh_token(data.refresh_token)
    if not user_id_str:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired refresh token")
    user = await get_user_by_id(db, UUID(user_id_str))
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found or inactive")
    tokens = get_tokens_for_user(user_id_str)
    return TokenResponse(**tokens)


@router.post("/forgot-password")
async def forgot_password(
    data: ForgotPasswordRequest,
    db: AsyncSession = Depends(get_db),
):
    """Send reset password email."""
    user = await get_user_by_email(db, data.email)
    if user and user.is_active:
        await set_reset_password_token(db, user)
    return {"message": "If the email exists, a reset link has been sent."}


@router.post("/reset-password")
async def reset_password_route(
    data: ResetPasswordRequest,
    db: AsyncSession = Depends(get_db),
):
    """Reset password with token from email."""
    user_id_str = verify_reset_token(data.token)
    if not user_id_str:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token")
    user = await reset_password(db, UUID(user_id_str), data.new_password)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")
    return {"message": "Password has been reset."}

