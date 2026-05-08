from typing import Any

from geojson_pydantic import (
    Feature,
    GeometryCollection,
    LineString,
    MultiLineString,
    MultiPoint,
    MultiPolygon,
    Point,
    Polygon,
)
from pydantic import BaseModel, Field

Geometry = (
    Point | MultiPoint | LineString | MultiLineString | Polygon | MultiPolygon | GeometryCollection
)


class ItemBase(BaseModel):
    geometry: Geometry
    properties: dict[str, Any] = Field(default_factory=dict)


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    geometry: Geometry | None = None
    properties: dict[str, Any] | None = None


class ItemRead(Feature):
    pass
