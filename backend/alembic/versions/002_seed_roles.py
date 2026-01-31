"""Seed default roles: user, admin.

Revision ID: 002_seed_roles
Revises: 001_initial
Create Date: 2025-01-31

"""
from typing import Sequence, Union
import uuid

from alembic import op
import sqlalchemy as sa

revision: str = "002_seed_roles"
down_revision: Union[str, None] = "001_initial"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Use fixed UUIDs so we can reference them in code
    op.execute(
        sa.text(
            """
            INSERT INTO roles (id, name, description)
            VALUES
                ('11111111-1111-1111-1111-111111111111', 'user', 'Standard user'),
                ('22222222-2222-2222-2222-222222222222', 'admin', 'Administrator')
            ON CONFLICT (name) DO NOTHING
            """
        )
    )


def downgrade() -> None:
    op.execute(
        sa.text(
            "DELETE FROM roles WHERE name IN ('user', 'admin')"
        )
    )
