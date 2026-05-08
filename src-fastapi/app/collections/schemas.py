from datetime import datetime
from typing import Annotated, Any
from geojson_pydantic.types import BBox
from pydantic import BaseModel, ConfigDict, Field, StringConstraints
from app.collections.constants import (
    COLLECTION_CRS_MAX_LENGTH,
    COLLECTION_DESCRIPTION_MAX_LENGTH,
    COLLECTION_ID_MAX_LENGTH,
    COLLECTION_SCHEMA_NAME_MAX_LENGTH,
    COLLECTION_TABLE_NAME_MAX_LENGTH,
    COLLECTION_TITLE_MAX_LENGTH,
    COLLECTION_GEOMETRY_COLUMN_MAX_LENGTH,
    COLLECTION_ID_COLUMN_MAX_LENGTH,
    COLLECTION_GEOMETRY_TYPE_MAX_LENGTH,
    COLLECTION_ERROR_MESSAGE_MAX_LENGTH,
    GeometryType,
)
from config import get_settings
from app.collections.models import CollectionStatus

settings = get_settings()

CollectionID = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        to_lower=True,
        min_length=1,
        max_length=COLLECTION_ID_MAX_LENGTH,
        pattern="^[a-z][a-z0-9_]*$",
    ),
]
CollectionTitle = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=COLLECTION_TITLE_MAX_LENGTH),
]


class CollectionBase(BaseModel):
    collection_id: CollectionID = Field(...)
    title: CollectionTitle = Field(...)
    description: str | None = Field(default=None, max_length=COLLECTION_DESCRIPTION_MAX_LENGTH)
    crs: str = Field(
        default_factory=lambda: settings.default_crs,
        max_length=COLLECTION_CRS_MAX_LENGTH,
    )
    schema_name: str = Field(
        default_factory=lambda: settings.default_schema_name,
        max_length=COLLECTION_SCHEMA_NAME_MAX_LENGTH,
    )
    table_name: str = Field(max_length=COLLECTION_TABLE_NAME_MAX_LENGTH)
    geometry_column: str = Field(
        default_factory=lambda: settings.default_geometry_column,
        max_length=COLLECTION_GEOMETRY_COLUMN_MAX_LENGTH,
    )
    id_column: str = Field(
        default_factory=lambda: settings.default_id_column,
        max_length=COLLECTION_ID_COLUMN_MAX_LENGTH,
    )
    srid: int = Field(default_factory=lambda: settings.default_srid)


class CollectionCreate(CollectionBase):
    pass


class CollectionReplace(CollectionBase):
    pass


class CollectionUpdate(BaseModel):
    title: CollectionTitle | None = Field(default=None)
    description: str | None = Field(default=None, max_length=COLLECTION_DESCRIPTION_MAX_LENGTH)
    crs: str | None = Field(default=None, max_length=COLLECTION_CRS_MAX_LENGTH)


class SpatialExtent(BaseModel):
    bbox: list[BBox] = Field(..., description="Bounding boxes (minx, miny, maxx, maxy)")
    crs: str = Field(default_factory=lambda: settings.default_crs)


class Extent(BaseModel):
    spatial: SpatialExtent | None = None


class CollectionRead(CollectionBase):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
    id: int = Field(...)
    project_id: int = Field(...)
    status: CollectionStatus = Field(...)
    feature_count: int = Field(...)
    geometry_type: GeometryType | None = Field(
        default=None, max_length=COLLECTION_GEOMETRY_TYPE_MAX_LENGTH
    )
    extent: Extent | None = Field(default=None, validation_alias="spatial_extent")
    source_metadata: dict[str, Any] = Field(...)
    error_message: str | None = Field(default=None, max_length=COLLECTION_ERROR_MESSAGE_MAX_LENGTH)
    last_import_at: datetime | None = Field(default=None)
    created_at: datetime = Field(...)
    updated_at: datetime = Field(...)
