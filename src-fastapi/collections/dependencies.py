from typing import Annotated

from fastapi import Depends

from database import DatabaseSessionDependency
from collections.repository import CollectionRepository
from collections.service import CollectionService


def get_collection_repository(
    session: DatabaseSessionDependency,
) -> CollectionRepository:
    return CollectionRepository(session)


CollectionRepositoryDependency = Annotated[
    CollectionRepository,
    Depends(get_collection_repository),
]


def get_collection_service(
    repository: CollectionRepositoryDependency,
) -> CollectionService:
    return CollectionService(repository)


CollectionServiceDependency = Annotated[
    CollectionService,
    Depends(get_collection_service),
]
