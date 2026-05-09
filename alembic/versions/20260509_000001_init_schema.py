"""init schema

Revision ID: 20260509_000001
Revises:
Create Date: 2026-05-09 00:00:01
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20260509_000001"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "channels",
        sa.Column("channel_id", sa.BigInteger(), nullable=False),
        sa.Column("author_id", sa.BigInteger(), nullable=False),
        sa.Column("channel_username", sa.String(length=255), nullable=True),
        sa.Column("title", sa.String(length=256), nullable=False),
        sa.Column("author_username", sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint("channel_id"),
    )
    op.create_table(
        "messages",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("text", sa.String(length=4096), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "buttons",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("text", sa.String(length=255), nullable=False),
        sa.Column("url", sa.String(length=256), nullable=False),
        sa.Column("column", sa.Integer(), nullable=False),
        sa.Column("row", sa.Integer(), nullable=False),
        sa.Column("message_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["message_id"], ["messages.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("buttons")
    op.drop_table("messages")
    op.drop_table("channels")
