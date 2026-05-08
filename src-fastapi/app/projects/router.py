
from fastapi import APIRouter, status

from app.projects.dependencies import ProjectServiceDependency
from app.projects.schemas import (
    ProjectCreate,
    ProjectRead,
    ProjectReplace,
    ProjectUpdate,
)


router = APIRouter(prefix="/projects", tags=["projects"])


@router.post(
    "/",
    response_model=ProjectRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_project(
    project: ProjectCreate,
    service: ProjectServiceDependency,
) -> ProjectRead:
    return ProjectRead.model_validate(await service.create(project))


@router.get(
    "/",
    response_model=list[ProjectRead],
    status_code=status.HTTP_200_OK,
)
async def list_projects(service: ProjectServiceDependency) -> list[ProjectRead]:
    return [ProjectRead.model_validate(project) for project in await service.list_all()]


@router.get(
    "/{project_id}",
    response_model=ProjectRead,
    status_code=status.HTTP_200_OK,
)
async def read_project(
    project_id: int,
    service: ProjectServiceDependency,
) -> ProjectRead:
    return ProjectRead.model_validate(await service.get(project_id))


@router.put(
    "/{project_id}",
    response_model=ProjectRead,
    status_code=status.HTTP_200_OK,
)
async def replace_project(
    project_id: int,
    project: ProjectReplace,
    service: ProjectServiceDependency,
) -> ProjectRead:
    return ProjectRead.model_validate(await service.replace(project_id, project))


@router.patch(
    "/{project_id}",
    response_model=ProjectRead,
    status_code=status.HTTP_200_OK,
)
async def update_project(
    project_id: int,
    project: ProjectUpdate,
    service: ProjectServiceDependency,
) -> ProjectRead:
    return ProjectRead.model_validate(await service.update(project_id, project))


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: int,
    service: ProjectServiceDependency,
) -> None:
    await service.delete(project_id)
