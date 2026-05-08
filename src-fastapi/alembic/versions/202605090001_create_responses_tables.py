"""create response_conversations and responses tables

Revision ID: 202605090001
Revises: 202605080002
Create Date: 2026-05-09 00:00:00
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


revision: str = "202605090001"
down_revision: str | Sequence[str] | None = "202605080002"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "response_conversations",
        sa.Column("id", sa.String(length=128), nullable=False),
        sa.Column("project_id", sa.Integer(), nullable=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("metadata_", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["project_id"], ["projects.id"], ondelete="SET NULL"
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "responses",
        sa.Column("id", sa.String(length=128), nullable=False),
        sa.Column("conversation_id", sa.String(length=128), nullable=False),
        sa.Column("previous_response_id", sa.String(length=128), nullable=True),
        sa.Column("model", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("instructions", sa.Text(), nullable=True),
        sa.Column("input_items", sa.Text(), nullable=True),
        sa.Column("output_items", sa.Text(), nullable=True),
        sa.Column("temperature", sa.Integer(), nullable=True),
        sa.Column("top_p", sa.Integer(), nullable=True),
        sa.Column("max_output_tokens", sa.Integer(), nullable=True),
        sa.Column("usage_prompt_tokens", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("usage_completion_tokens", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("usage_total_tokens", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("error_code", sa.String(length=64), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("duration_ms", sa.Integer(), nullable=True),
        sa.Column("store", sa.Integer(), nullable=False, server_default=sa.text("1")),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["conversation_id"], ["response_conversations.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index("ix_responses_status", "responses", ["status"])
    op.create_index("ix_responses_conversation_id", "responses", ["conversation_id"])


def downgrade() -> None:
    op.drop_index("ix_responses_conversation_id", table_name="responses")
    op.drop_index("ix_responses_status", table_name="responses")
    op.drop_table("responses")
    op.drop_table("response_conversations")