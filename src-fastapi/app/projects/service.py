from typing import NoReturn

from fastapi import HTTPException, status

from app.projects.models import Project
from app.projects.repository import ProjectRepository
from app.projects.schemas import ProjectCreate, ProjectReplace, ProjectUpdate


class ProjectService:
    def __init__(self, repository: ProjectRepository) -> None:
        self.repository = repository

    async def create(self, project: ProjectCreate) -> Project:
        return await self.repository.create(project)

    async def list_all(self) -> list[Project]:
        return await self.repository.list_all()

    async def get(self, project_id: int) -> Project:
        project = await self.repository.get(project_id)
        if project is None:
            raise_project_not_found(project_id)
        return project

    async def replace(self, project_id: int, project: ProjectReplace) -> Project:
        updated_project = await self.repository.replace(project_id, project)
        if updated_project is None:
            raise_project_not_found(project_id)
        return updated_project

    async def update(self, project_id: int, project: ProjectUpdate) -> Project:
        updated_project = await self.repository.update(project_id, project)
        if updated_project is None:
            raise_project_not_found(project_id)
        return updated_project

    async def delete(self, project_id: int) -> None:
        if not await self.repository.delete(project_id):
            raise_project_not_found(project_id)


def raise_project_not_found(identifier: str | int) -> NoReturn:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"message": "Project not found", "identifier": str(identifier)},
    )
