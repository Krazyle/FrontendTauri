from datetime import UTC, datetime

from sqlalchemy import CheckConstraint, Column, DateTime, String, event, func
from sqlmodel import Field, SQLModel

from app.projects.constants import PROJECT_DESCRIPTION_MAX_LENGTH, PROJECT_NAME_MAX_LENGTH


def utc_now() -> datetime:
    return datetime.now(UTC)


class Project(SQLModel, table=True):
    __tablename__ = "projects"
    __table_args__ = (
        CheckConstraint("length(trim(name)) >= 1", name="ck_projects_name_not_blank"),
    )

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(
        sa_column=Column(
            String(PROJECT_NAME_MAX_LENGTH),
            index=True,
            nullable=False,
        ),
    )
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


# Keeps ORM mutations consistent across drivers; Column.onupdate covers
# SQLAlchemy-generated UPDATEs, but the mapper hook updates the entity too.
@event.listens_for(Project, "before_update")
def update_project_timestamp(
    _mapper: object,
    _connection: object,
    project: Project,
) -> None:
    project.updated_at = utc_now()
