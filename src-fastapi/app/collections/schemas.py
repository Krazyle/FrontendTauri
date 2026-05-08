from datetime import datetime
from typing import Annotated, Any

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
    OGC_CRS84,
    DEFAULT_SCHEMA_NAME,
    DEFAULT_GEOMETRY_COLUMN,
    DEFAULT_ID_COLUMN,
    DEFAULT_SRID,
)
from app.collections.models import CollectionStatus

CollectionID = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        to_lower=True,
        min_length=1,
        max_length=COLLECTION_ID_MAX_LENGTH,
        pattern=r"^[a-z][a-z0-9_]*$",
    ),
]

CollectionTitle = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=1,
        max_length=COLLECTION_TITLE_MAX_LENGTH,
    ),
]


class CollectionBase(BaseModel):
    collection_id: CollectionID
    title: CollectionTitle
    description: str | None = Field(
        default=None,
        max_length=COLLECTION_DESCRIPTION_MAX_LENGTH,
    )
    crs: str = Field(
        default=OGC_CRS84,
        max_length=COLLECTION_CRS_MAX_LENGTH,
    )
    schema_name: str = Field(
        default=DEFAULT_SCHEMA_NAME,
        max_length=COLLECTION_SCHEMA_NAME_MAX_LENGTH,
    )
    table_name: str = Field(
        max_length=COLLECTION_TABLE_NAME_MAX_LENGTH,
    )
    geometry_column: str = Field(
        default=DEFAULT_GEOMETRY_COLUMN,
        max_length=COLLECTION_GEOMETRY_COLUMN_MAX_LENGTH,
    )
    id_column: str = Field(
        default=DEFAULT_ID_COLUMN,
        max_length=COLLECTION_ID_COLUMN_MAX_LENGTH,
    )
    srid: int = DEFAULT_SRID


class CollectionCreate(CollectionBase):
    pass


class CollectionReplace(CollectionBase):
    pass


class CollectionUpdate(BaseModel):
    title: CollectionTitle | None = None
    description: str | None = Field(
        default=None,
        max_length=COLLECTION_DESCRIPTION_MAX_LENGTH,
    )
    crs: str | None = Field(
        default=None,
        max_length=COLLECTION_CRS_MAX_LENGTH,
    )


class CollectionRead(CollectionBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    project_id: int
    status: CollectionStatus
    feature_count: int
    geometry_type: str | None = Field(
        default=None,
        max_length=COLLECTION_GEOMETRY_TYPE_MAX_LENGTH,
    )
    spatial_extent: dict[str, Any] | None = None
    source_metadata: dict[str, Any]
    error_message: str | None = Field(
        default=None,
        max_length=COLLECTION_ERROR_MESSAGE_MAX_LENGTH,
    )
    last_import_at: datetime | None = None
    created_at: datetime
    updated_at: datetime
