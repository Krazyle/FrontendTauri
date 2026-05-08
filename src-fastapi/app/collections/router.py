
from fastapi import APIRouter, status

from app.collections.dependencies import CollectionServiceDependency
from app.collections.schemas import (
    CollectionCreate,
    CollectionRead,
    CollectionReplace,
    CollectionUpdate,
)


router = APIRouter(prefix="/projects/{project_id}/collections", tags=["collections"])


@router.get(
    "/",
    response_model=list[CollectionRead],
    status_code=status.HTTP_200_OK,
)
async def list_collections(
    project_id: int,
    service: CollectionServiceDependency,
) -> list[CollectionRead]:
    return [
        CollectionRead.model_validate(c)
        for c in await service.list_by_project(project_id)
    ]


@router.get(
    "/{id}",
    response_model=CollectionRead,
    status_code=status.HTTP_200_OK,
)
async def get_collection(
    project_id: int,
    id: int,
    service: CollectionServiceDependency,
) -> CollectionRead:
    return CollectionRead.model_validate(await service.get(project_id, id))


@router.post(
    "/",
    response_model=CollectionRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_collection(
    project_id: int,
    collection: CollectionCreate,
    service: CollectionServiceDependency,
) -> CollectionRead:
    return CollectionRead.model_validate(await service.create(project_id, collection))


@router.put(
    "/{id}",
    response_model=CollectionRead,
    status_code=status.HTTP_200_OK,
)
async def replace_collection(
    project_id: int,
    id: int,
    collection: CollectionReplace,
    service: CollectionServiceDependency,
) -> CollectionRead:
    return CollectionRead.model_validate(await service.replace(project_id, id, collection))


@router.patch(
    "/{id}",
    response_model=CollectionRead,
    status_code=status.HTTP_200_OK,
)
async def update_collection(
    project_id: int,
    id: int,
    collection: CollectionUpdate,
    service: CollectionServiceDependency,
) -> CollectionRead:
    return CollectionRead.model_validate(await service.update(project_id, id, collection))


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_collection(
    project_id: int,
    id: int,
    service: CollectionServiceDependency,
) -> None:
    await service.delete(project_id, id)
