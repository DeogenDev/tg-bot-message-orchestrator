"""add entities column to messages

Revision ID: 20260510_000003
Revises: 20260510_000002
Create Date: 2026-05-10 00:00:03
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20260510_000003"
down_revision: Union[str, Sequence[str], None] = "20260510_000002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("messages", sa.Column("entities", sa.JSON(), nullable=True))


def downgrade() -> None:
    op.drop_column("messages", "entities")
