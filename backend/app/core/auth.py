"""Login logic, token creation, refresh."""
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    get_password_hash,
    verify_password,
)
from app.config import get_settings


def get_tokens_for_user(user_id: str) -> dict:
    settings = get_settings()
    access = create_access_token(user_id)
    refresh = create_refresh_token(user_id)
    return {
        "access_token": access,
        "refresh_token": refresh,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    }


def authenticate_user(plain_password: str, hashed_password: str) -> bool:
    return verify_password(plain_password, hashed_password)


def hash_password(password: str) -> str:
    return get_password_hash(password)


def verify_refresh_token(token: str) -> str | None:
    payload = decode_token(token)
    if payload and payload.get("type") == "refresh":
        return payload.get("sub")
    return None


def verify_reset_token(token: str) -> str | None:
    payload = decode_token(token)
    if payload and payload.get("type") == "reset":
        return payload.get("sub")
    return None
