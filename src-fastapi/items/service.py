from uuid import UUID
from typing import Any, NoReturn

from fastapi import HTTPException, status

from collections.service import CollectionService
from items.repository import ItemRepository
from items.schemas import ItemCreate, ItemUpdate


class ItemService:
    def __init__(
        self,
        repository: ItemRepository,
        collection_service: CollectionService,
    ) -> None:
        self.repository = repository
        self.collection_service = collection_service

    async def create(
        self,
        project_id: UUID,
        collection_id: UUID,
        item: ItemCreate,
    ) -> dict[str, Any]:
        collection = await self.collection_service.get(project_id, collection_id)
        return await self.repository.create(collection, item)

    async def get(
        self,
        project_id: UUID,
        collection_id: UUID,
        feature_id: str | int,
    ) -> dict[str, Any]:
        collection = await self.collection_service.get(project_id, collection_id)
        item = await self.repository.get(collection, feature_id)
        if item is None:
            raise_item_not_found(feature_id)
        return item

    async def update(
        self,
        project_id: UUID,
        collection_id: UUID,
        feature_id: str | int,
        item: ItemUpdate,
    ) -> dict[str, Any]:
        collection = await self.collection_service.get(project_id, collection_id)
        updated = await self.repository.update(collection, feature_id, item)
        if updated is None:
            raise_item_not_found(feature_id)
        return updated

    async def delete(
        self,
        project_id: UUID,
        collection_id: UUID,
        feature_id: str | int,
    ) -> None:
        collection = await self.collection_service.get(project_id, collection_id)
        if not await self.repository.delete(collection, feature_id):
            raise_item_not_found(feature_id)


def raise_item_not_found(identifier: str | int) -> NoReturn:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={
            "message": "Item not found",
            "identifier": str(identifier),
        },
    )
