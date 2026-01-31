"""Role schemas."""
from uuid import UUID

from pydantic import BaseModel


class RoleBase(BaseModel):
    name: str
    description: str | None = None


class RoleResponse(RoleBase):
    id: UUID

    class Config:
        from_attributes = True
