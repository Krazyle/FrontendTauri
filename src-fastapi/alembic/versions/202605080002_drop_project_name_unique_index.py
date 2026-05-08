"""drop project name unique index

Revision ID: 202605080002
Revises: 202605080001
Create Date: 2026-05-08 00:00:00
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


revision: str = "202605080002"
down_revision: str | Sequence[str] | None = "202605080001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute(sa.text("DROP INDEX IF EXISTS ix_projects_name_lower_unique"))


def downgrade() -> None:
    pass
