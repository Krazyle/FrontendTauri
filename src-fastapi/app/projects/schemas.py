from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

from app.projects.constants import (
    PROJECT_DESCRIPTION_MAX_LENGTH,
    PROJECT_NAME_MAX_LENGTH,
)


ProjectName = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=1,
        max_length=PROJECT_NAME_MAX_LENGTH,
    ),
]


class ProjectBase(BaseModel):
    name: ProjectName
    description: str | None = Field(
        default=None,
        max_length=PROJECT_DESCRIPTION_MAX_LENGTH,
    )


class ProjectCreate(ProjectBase):
    pass


class ProjectReplace(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: ProjectName | None = None
    description: str | None = Field(
        default=None,
        max_length=PROJECT_DESCRIPTION_MAX_LENGTH,
    )


class ProjectRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: ProjectName
    description: str | None = None
    created_at: datetime
    updated_at: datetime
