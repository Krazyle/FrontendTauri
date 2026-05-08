from typing import Any

from pydantic import BaseModel, Field


class ItemBase(BaseModel):
    geometry: dict[str, Any]
    properties: dict[str, Any] = Field(default_factory=dict)


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    geometry: dict[str, Any] | None = None
    properties: dict[str, Any] | None = None


class ItemRead(ItemBase):
    id: str | int
    type: str = "Feature"
