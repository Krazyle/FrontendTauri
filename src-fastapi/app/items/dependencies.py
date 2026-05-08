from typing import Annotated
from fastapi import Depends
from database import DatabaseSessionDependency
from app.items.repository import ItemRepository
from app.items.service import ItemService
from app.collections.dependencies import CollectionServiceDependency


def get_item_repository(session: DatabaseSessionDependency) -> ItemRepository:
    return ItemRepository(session)


ItemRepositoryDependency = Annotated[ItemRepository, Depends(get_item_repository)]


def get_item_service(
    repository: ItemRepositoryDependency,
    collection_service: CollectionServiceDependency,
) -> ItemService:
    return ItemService(repository, collection_service)


ItemServiceDependency = Annotated[ItemService, Depends(get_item_service)]
