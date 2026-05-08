from typing import NoReturn
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from app.collections.models import Collection
from app.collections.repository import CollectionRepository
from app.collections.schemas import CollectionCreate, CollectionReplace, CollectionUpdate


class CollectionService:
    def __init__(self, repository: CollectionRepository) -> None:
        self.repository = repository

    async def create(self, project_id: int, collection: CollectionCreate) -> Collection:
        try:
            return await self.repository.create(project_id, collection)
        except IntegrityError as e:
            raise_collection_conflict(e)

    async def list_by_project(self, project_id: int) -> list[Collection]:
        return await self.repository.list_by_project(project_id)

    async def get(self, project_id: int, id: int) -> Collection:
        collection = await self.repository.get(project_id, id)
        if collection is None:
            raise_collection_not_found(id)
        return collection

    async def get_by_identifier(self, project_id: int, collection_id: str) -> Collection:
        collection = await self.repository.get_by_identifier(project_id, collection_id)
        if collection is None:
            raise_collection_not_found(collection_id)
        return collection

    async def replace(self, project_id: int, id: int, collection: CollectionReplace) -> Collection:
        try:
            updated = await self.repository.replace(project_id, id, collection)
            if updated is None:
                raise_collection_not_found(id)
            return updated
        except IntegrityError as e:
            raise_collection_conflict(e)

    async def update(self, project_id: int, id: int, collection: CollectionUpdate) -> Collection:
        updated = await self.repository.update(project_id, id, collection)
        if updated is None:
            raise_collection_not_found(id)
        return updated

    async def delete(self, project_id: int, id: int) -> None:
        if not await self.repository.delete(project_id, id):
            raise_collection_not_found(id)


def raise_collection_not_found(identifier: int | str) -> NoReturn:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={
            "message": "Collection not found",
            "identifier": str(identifier),
        },
    )


def raise_collection_conflict(e: IntegrityError) -> NoReturn:
    error_msg = str(e.orig)
    detail = "A collection with this identifier or table name already exists."

    if "uq_project_collection" in error_msg:
        detail = "A collection with this ID already exists in this project."
    elif "uq_collection_table" in error_msg:
        detail = "A database table with this schema and name already exists."

    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail={
            "message": "Collection conflict",
            "reason": detail,
        },
    )
