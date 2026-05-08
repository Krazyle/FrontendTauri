from datetime import datetime

from sqlalchemy import CheckConstraint, Column, DateTime, String, func
from sqlmodel import Field, SQLModel
from app.projects.constants import (
    PROJECT_DESCRIPTION_MAX_LENGTH,
    PROJECT_NAME_MAX_LENGTH,
)
from app.utils import utc_now


class Project(SQLModel, table=True):
    __tablename__ = "projects"
    __table_args__ = (
        CheckConstraint("length(trim(name)) >= 1", name="ck_projects_name_not_blank"),
    )
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(sa_column=Column(String(PROJECT_NAME_MAX_LENGTH), index=True, nullable=False))
    description: str | None = Field(
        default=None,
        sa_column=Column(String(PROJECT_DESCRIPTION_MAX_LENGTH), nullable=True),
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
