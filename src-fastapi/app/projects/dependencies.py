from typing import Annotated

from fastapi import Depends

from database import DatabaseSessionDependency
from app.projects.repository import ProjectRepository
from app.projects.service import ProjectService


def get_project_repository(session: DatabaseSessionDependency) -> ProjectRepository:
    return ProjectRepository(session)


ProjectRepositoryDependency = Annotated[
    ProjectRepository,
    Depends(get_project_repository),
]


def get_project_service(
    repository: ProjectRepositoryDependency,
) -> ProjectService:
    return ProjectService(repository)


ProjectServiceDependency = Annotated[
    ProjectService,
    Depends(get_project_service),
]
