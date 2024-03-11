"""Add updated_at and deleted_at fields to user model

Revision ID: 78dbaa9565a3
Revises: 2c7d62e29370
Create Date: 2024-03-11 19:47:05.321624

"""

from collections.abc import Sequence
from datetime import datetime

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "78dbaa9565a3"
down_revision: str | None = "2c7d62e29370"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    updated_at = sa.Column("updated_at", sa.DateTime(), nullable=True)
    deleted_at = sa.Column("deleted_at", sa.DateTime(), nullable=True)

    op.add_column("users", updated_at)
    op.add_column("users", deleted_at)


def downgrade() -> None:
    op.drop_column("users", "updated_at")
    op.drop_column("users", "deleted_at")
