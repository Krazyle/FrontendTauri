from datetime import datetime
from typing import Any

import secrets
import time

from sqlalchemy import Column, DateTime, ForeignKey, Integer, JSON, String, Text, func
from sqlmodel import Field, SQLModel

from app.responses.constants import ID_RESPONSE_PREFIX
from app.utils import utc_now


def _generate_response_id() -> str:
    ts = int(time.time() * 1000)
    rand = secrets.token_hex(12)
    return f"{ID_RESPONSE_PREFIX}{ts:x}{rand[:8]}"


class Response(SQLModel, table=True):
    __tablename__ = "responses"

    id: str = Field(
        default_factory=_generate_response_id,
        sa_column=Column(String(128), primary_key=True),
    )
    conversation_id: str = Field(
        sa_column=Column(
            String(128),
            ForeignKey("response_conversations.id", ondelete="CASCADE"),
            nullable=False,
        )
    )
    previous_response_id: str | None = Field(
        default=None, sa_column=Column(String(128), nullable=True)
    )
    model: str = Field(sa_column=Column(String(255), nullable=False))
    status: str = Field(default="queued", sa_column=Column(String(32), nullable=False, index=True))
    instructions: str | None = Field(default=None, sa_column=Column(Text, nullable=True))
    input_items: list[dict[str, Any]] | None = Field(
        default=None, sa_column=Column(JSON, nullable=True)
    )
    output_items: list[dict[str, Any]] | None = Field(
        default=None, sa_column=Column(JSON, nullable=True)
    )
    temperature: float | None = Field(default=None, sa_column=Column(Integer, nullable=True))
    top_p: float | None = Field(default=None, sa_column=Column(Integer, nullable=True))
    max_output_tokens: int | None = Field(default=None, sa_column=Column(Integer, nullable=True))
    usage_prompt_tokens: int = Field(default=0, sa_column=Column(Integer, nullable=False))
    usage_completion_tokens: int = Field(default=0, sa_column=Column(Integer, nullable=False))
    usage_total_tokens: int = Field(default=0, sa_column=Column(Integer, nullable=False))
    error_code: str | None = Field(default=None, sa_column=Column(String(64), nullable=True))
    error_message: str | None = Field(default=None, sa_column=Column(Text, nullable=True))
    duration_ms: int | None = Field(default=None, sa_column=Column(Integer, nullable=True))
    store: bool = Field(default=True, sa_column=Column(Integer, nullable=False))
    created_at: datetime = Field(
        default_factory=utc_now,
        sa_column=Column(
            DateTime(timezone=True),
            default=utc_now,
            server_default=func.now(),
            nullable=False,
        ),
    )
    completed_at: datetime | None = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), nullable=True),
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
