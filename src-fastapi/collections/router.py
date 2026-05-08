from uuid import UUID

from fastapi import APIRouter, status

from collections.dependencies import CollectionServiceDependency
from collections.schemas import (
    CollectionCreate,
    CollectionRead,
    CollectionReplace,
    CollectionUpdate,
)


router = APIRouter(prefix="/projects/{project_id}/collections", tags=["collections"])


@router.post(
    "/",
    response_model=CollectionRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_collection(
    project_id: UUID,
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
    project_id: UUID,
    id: UUID,
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
    project_id: UUID,
    id: UUID,
    collection: CollectionUpdate,
    service: CollectionServiceDependency,
) -> CollectionRead:
    return CollectionRead.model_validate(await service.update(project_id, id, collection))


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_collection(
    project_id: UUID,
    id: UUID,
    service: CollectionServiceDependency,
) -> None:
    await service.delete(project_id, id)
