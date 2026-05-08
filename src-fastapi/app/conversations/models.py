from __future__ import annotations

import secrets
import time
from datetime import datetime
from typing import Any

from sqlalchemy import Column, DateTime, ForeignKey, Integer, JSON, String, func
from sqlmodel import Field, SQLModel

from app.conversations.constants import ID_CONVERSATION_PREFIX
from app.utils import utc_now


def _generate_conversation_id() -> str:
    ts = int(time.time() * 1000)
    rand = secrets.token_hex(12)
    return f"{ID_CONVERSATION_PREFIX}{ts:x}{rand[:8]}"


class Conversation(SQLModel, table=True):
    __tablename__ = "response_conversations"

    id: str = Field(
        default_factory=_generate_conversation_id,
        sa_column=Column(String(128), primary_key=True),
    )
    project_id: int | None = Field(
        default=None,
        sa_column=Column(Integer, ForeignKey("projects.id", ondelete="SET NULL"), nullable=True),
    )
    title: str = Field(default="New Conversation", sa_column=Column(String(255), nullable=False))
    metadata_: dict[str, Any] | None = Field(
        default=None,
        sa_column=Column("metadata_", JSON, nullable=True),
        alias="metadata",
    )
    created_at: datetime = Field(
        default_factory=utc_now,
        sa_column=Column(
            DateTime(timezone=True),
            default=utc_now,
            server_default=func.now(),
            nullable=False,
        ),
    )
    updated_at: datetime = Field(
        default_factory=utc_now,
        sa_column=Column(
            DateTime(timezone=True),
            default=utc_now,
            server_default=func.now(),
            onupdate=utc_now,
            nullable=False,
        ),
    )
