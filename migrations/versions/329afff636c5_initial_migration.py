"""initial migration

Revision ID: 329afff636c5
Revises: 
Create Date: 2024-02-03 19:17:16.236633

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "329afff636c5"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("username", sa.String(100), unique=True, nullable=False),
        sa.Column("password", sa.String(100), nullable=False),
    )

    op.create_table(
        "calculation_history",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False),
        sa.Column("file_name", sa.String(100), nullable=False),
        sa.Column("date", sa.DateTime, nullable=False, default=sa.func.now()),
        sa.Column("successful", sa.Boolean, nullable=False, default=sa.false()),
        sa.Column("result", sa.JSON),
        sa.Column("errors", sa.JSON),
    )


def downgrade():
    op.drop_table("calculation_history")
    op.drop_table("users")
