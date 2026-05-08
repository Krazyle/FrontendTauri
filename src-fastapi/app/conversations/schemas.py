from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from app.responses.schemas import ResponseRead


class ConversationCreate(BaseModel):
    title: str = "New Conversation"
    project_id: int | None = None
    metadata: dict[str, str] | None = Field(default=None, serialization_alias="metadata")


class ConversationUpdate(BaseModel):
    title: str | None = None
    project_id: int | None = None
    metadata: dict[str, str] | None = Field(default=None, serialization_alias="metadata")


class ConversationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    project_id: int | None = None
    title: str
    metadata_: dict[str, Any] | None = Field(default=None, alias="metadata")
    created_at: datetime
    updated_at: datetime


class ConversationWithResponses(ConversationRead):
    responses: list[ResponseRead] = Field(default_factory=list)
