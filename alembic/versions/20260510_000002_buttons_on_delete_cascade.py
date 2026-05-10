"""add on delete cascade for buttons.message_id

Revision ID: 20260510_000002
Revises: 20260509_000001
Create Date: 2026-05-10 00:00:02
"""

from typing import Sequence, Union

from alembic import op


revision: str = "20260510_000002"
down_revision: Union[str, Sequence[str], None] = "20260509_000001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint("buttons_message_id_fkey", "buttons", type_="foreignkey")
    op.create_foreign_key(
        "buttons_message_id_fkey",
        "buttons",
        "messages",
        ["message_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint("buttons_message_id_fkey", "buttons", type_="foreignkey")
    op.create_foreign_key(
        "buttons_message_id_fkey",
        "buttons",
        "messages",
        ["message_id"],
        ["id"],
    )
