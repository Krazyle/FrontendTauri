from typing import Any, NoReturn
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from app.collections.service import CollectionService
from app.items.repository import ItemRepository
from app.items.schemas import ItemCreate, ItemUpdate


class ItemService:
    def __init__(self, repository: ItemRepository, collection_service: CollectionService) -> None:
        self.repository = repository
        self.collection_service = collection_service

    async def create(self, project_id: int, collection_id: int, item: ItemCreate) -> dict[str, Any]:
        collection = await self.collection_service.get(project_id, collection_id)
        self._validate_geometry_type(collection, item.geometry)
        try:
            created = await self.repository.create(collection, item)
            if created is None:
                raise_item_not_found("N/A")
            return created
        except IntegrityError as e:
            raise_item_conflict(e)

    async def update(
        self,
        project_id: int,
        collection_id: int,
        feature_id: str | int,
        item: ItemUpdate,
    ) -> dict[str, Any]:
        collection = await self.collection_service.get(project_id, collection_id)
        if item.geometry:
            self._validate_geometry_type(collection, item.geometry)
        try:
            updated = await self.repository.update(collection, feature_id, item)
            if updated is None:
                raise_item_not_found(feature_id)
            return updated
        except IntegrityError as e:
            raise_item_conflict(e)

    async def delete(self, project_id: int, collection_id: int, feature_id: str | int) -> None:
        collection = await self.collection_service.get(project_id, collection_id)
        if not await self.repository.delete(collection, feature_id):
            raise_item_not_found(feature_id)

    def _validate_geometry_type(self, collection: Any, geometry: Any) -> None:
        if collection.geometry_type and geometry.type != collection.geometry_type.value:
            raise_geometry_type_mismatch(
                expected=collection.geometry_type.value, actual=geometry.type
            )


def raise_item_not_found(identifier: str | int) -> NoReturn:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"message": "Item not found", "identifier": str(identifier)},
    )


def raise_geometry_type_mismatch(expected: str, actual: str) -> NoReturn:
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail={
            "message": "Geometry type mismatch",
            "reason": f"This collection only accepts {expected} geometries.",
            "expected": expected,
            "actual": actual,
        },
    )


def raise_item_conflict(e: IntegrityError) -> NoReturn:
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail={
            "message": "Item conflict",
            "reason": "An item with this identifier already exists.",
            "details": str(e.orig),
        },
    )
