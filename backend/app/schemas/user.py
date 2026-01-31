"""User schemas."""
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    full_name: str | None = None


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    full_name: str | None = None


class UserInDB(UserBase):
    id: UUID
    is_active: bool
    email_verified: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserResponse(UserBase):
    id: UUID
    is_active: bool
    email_verified: bool
    created_at: datetime
    role_names: list[str] = []

    class Config:
        from_attributes = True
