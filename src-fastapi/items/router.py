from uuid import UUID

from fastapi import APIRouter, status

from items.dependencies import ItemServiceDependency
from items.schemas import ItemCreate, ItemRead, ItemUpdate


router = APIRouter(
    prefix="/projects/{project_id}/collections/{collection_id}/items",
    tags=["items"],
)


@router.post(
    "/",
    response_model=ItemRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_item(
    project_id: UUID,
    collection_id: UUID,
    item: ItemCreate,
    service: ItemServiceDependency,
) -> ItemRead:
    return ItemRead(**await service.create(project_id, collection_id, item))


@router.get(
    "/{feature_id}",
    response_model=ItemRead,
    status_code=status.HTTP_200_OK,
)
async def read_item(
    project_id: UUID,
    collection_id: UUID,
    feature_id: str,
    service: ItemServiceDependency,
) -> ItemRead:
    # We use str for feature_id as it could be integer or string depending on the table
    return ItemRead(**await service.get(project_id, collection_id, feature_id))


@router.patch(
    "/{feature_id}",
    response_model=ItemRead,
    status_code=status.HTTP_200_OK,
)
async def update_item(
    project_id: UUID,
    collection_id: UUID,
    feature_id: str,
    item: ItemUpdate,
    service: ItemServiceDependency,
) -> ItemRead:
    return ItemRead(**await service.update(project_id, collection_id, feature_id, item))


@router.delete("/{feature_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
    project_id: UUID,
    collection_id: UUID,
    feature_id: str,
    service: ItemServiceDependency,
) -> None:
    await service.delete(project_id, collection_id, feature_id)
