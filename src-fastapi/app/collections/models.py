from datetime import datetime
from enum import Enum
from typing import Any
from pydantic import field_validator
from sqlalchemy import (
    CheckConstraint,
    Column,
    DateTime,
    Index,
    JSON,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, SQLModel
from app.collections.constants import (
    COLLECTION_CRS_MAX_LENGTH,
    COLLECTION_DESCRIPTION_MAX_LENGTH,
    COLLECTION_ERROR_MESSAGE_MAX_LENGTH,
    COLLECTION_GEOMETRY_COLUMN_MAX_LENGTH,
    COLLECTION_GEOMETRY_TYPE_MAX_LENGTH,
    COLLECTION_ID_COLUMN_MAX_LENGTH,
    COLLECTION_ID_MAX_LENGTH,
    COLLECTION_SCHEMA_NAME_MAX_LENGTH,
    COLLECTION_TABLE_NAME_MAX_LENGTH,
    COLLECTION_TITLE_MAX_LENGTH,
    GeometryType,
)
from app.utils import utc_now
from config import get_settings

settings = get_settings()

POSTGRES_JSON = JSON().with_variant(JSONB, "postgresql")


class CollectionStatus(str, Enum):
    IMPORTING = "importing"
    PUBLISHED = "published"
    FAILED = "failed"
    ARCHIVED = "archived"


class Collection(SQLModel, table=True):
    __tablename__ = "project_collections"
    __table_args__ = (
        UniqueConstraint("project_id", "collection_id", name="uq_project_collection"),
        UniqueConstraint("schema_name", "table_name", name="uq_collection_table"),
        Index("idx_collections_project_status", "project_id", "status"),
        Index("idx_collections_project_created", "project_id", "created_at"),
        Index("idx_collections_status", "status"),
        Index("idx_collections_updated_at", "updated_at"),
        CheckConstraint(
            "length(trim(collection_id)) >= 1",
            name="ck_collections_collection_id_not_blank",
        ),
        CheckConstraint("length(trim(title)) >= 1", name="ck_collections_title_not_blank"),
        CheckConstraint("feature_count >= 0", name="ck_feature_count_nonnegative"),
    )
    id: int | None = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="projects.id", ondelete="CASCADE", index=True)
    collection_id: str = Field(max_length=COLLECTION_ID_MAX_LENGTH)
    title: str = Field(max_length=COLLECTION_TITLE_MAX_LENGTH)
    description: str | None = Field(default=None, max_length=COLLECTION_DESCRIPTION_MAX_LENGTH)
    crs: str = Field(
        default_factory=lambda: settings.default_crs,
        max_length=COLLECTION_CRS_MAX_LENGTH,
    )
    spatial_extent: dict[str, Any] | None = Field(
        default=None, sa_column=Column(POSTGRES_JSON, nullable=True)
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
    srid: int = Field(default_factory=lambda: settings.default_srid, nullable=False)
    geometry_type: GeometryType | None = Field(
        default=None, max_length=COLLECTION_GEOMETRY_TYPE_MAX_LENGTH
    )
    feature_count: int = Field(default=0)
    source_metadata: dict[str, Any] = Field(
        default_factory=dict, sa_column=Column(POSTGRES_JSON, nullable=False)
    )
    status: CollectionStatus = Field(
        default_factory=lambda: CollectionStatus(settings.collections_default_import_status)
    )
    error_message: str | None = Field(default=None, max_length=COLLECTION_ERROR_MESSAGE_MAX_LENGTH)
    last_import_at: datetime | None = Field(
        default=None, sa_column=Column(DateTime(timezone=True), nullable=True)
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

    @field_validator("geometry_type", mode="before")
    @classmethod
    def validate_geometry_type(cls, value: Any) -> GeometryType | None:
        if value is None:
            return None
        if isinstance(value, GeometryType):
            return value
        if isinstance(value, str):
            mapping = {t.value.upper(): t for t in GeometryType}
            upper_value = value.upper()
            if upper_value in mapping:
                return mapping[upper_value]
            raise ValueError(f"Invalid geometry type: {value}")
        return value

    def __repr__(self) -> str:
        return (
            f"<Collection(id={self.id}, collection_id={self.collection_id}, status={self.status})>"
        )
