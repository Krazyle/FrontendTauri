from uuid import UUID
from typing import NoReturn

from fastapi import HTTPException, status

from projects.models import Project
from projects.repository import ProjectRepository
from projects.schemas import ProjectCreate, ProjectReplace, ProjectUpdate


class ProjectService:
    def __init__(self, repository: ProjectRepository) -> None:
        self.repository = repository

    async def create(self, project: ProjectCreate) -> Project:
        return await self.repository.create(project)

    async def list_all(self) -> list[Project]:
        return await self.repository.list_all()

    async def get(self, project_id: UUID) -> Project:
        project = await self.repository.get(project_id)
        if project is None:
            raise_project_not_found()
        return project

    async def replace(self, project_id: UUID, project: ProjectReplace) -> Project:
        updated_project = await self.repository.replace(project_id, project)

        if updated_project is None:
            raise_project_not_found()
        return updated_project

    async def update(self, project_id: UUID, project: ProjectUpdate) -> Project:
        updated_project = await self.repository.update(project_id, project)

        if updated_project is None:
            raise_project_not_found()
        return updated_project

    async def delete(self, project_id: UUID) -> None:
        if not await self.repository.delete(project_id):
            raise_project_not_found()


def raise_project_not_found() -> NoReturn:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Project not found",
    )
