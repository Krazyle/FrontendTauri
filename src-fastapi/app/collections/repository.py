from sqlalchemy import select, and_, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import col
from app.collections.models import Collection
from app.collections.schemas import (
    CollectionCreate,
    CollectionReplace,
    CollectionUpdate,
)


class CollectionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, project_id: int, collection: CollectionCreate) -> Collection:
        created_collection = Collection(project_id=project_id, **collection.model_dump())
        self.session.add(created_collection)
        await self.session.commit()
        await self.session.refresh(created_collection)
        return created_collection

    async def list_by_project(self, project_id: int) -> list[Collection]:
        statement = (
            select(Collection)
            .where(col(Collection.project_id) == project_id)
            .order_by(col(Collection.created_at), col(Collection.id))
        )
        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def get(self, project_id: int, id: int) -> Collection | None:
        statement = select(Collection).where(
            and_(col(Collection.project_id) == project_id, col(Collection.id) == id)
        )
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def get_by_identifier(self, project_id: int, collection_id: str) -> Collection | None:
        statement = select(Collection).where(
            and_(
                col(Collection.project_id) == project_id,
                col(Collection.collection_id) == collection_id,
            )
        )
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def replace(
        self, project_id: int, id: int, collection: CollectionReplace
    ) -> Collection | None:
        existing = await self.get(project_id, id)
        if existing is None:
            return None
        replace_data = collection.model_dump()
        for key, value in replace_data.items():
            setattr(existing, key, value)
        await self.session.commit()
        await self.session.refresh(existing)
        return existing

    async def update(
        self, project_id: int, id: int, collection: CollectionUpdate
    ) -> Collection | None:
        existing = await self.get(project_id, id)
        if existing is None:
            return None
        update_data = collection.model_dump(exclude_unset=True)
        if not update_data:
            return existing
        for key, value in update_data.items():
            setattr(existing, key, value)
        await self.session.commit()
        await self.session.refresh(existing)
        return existing

    async def delete(self, project_id: int, id: int) -> bool:
        statement = (
            delete(Collection)
            .where(and_(col(Collection.project_id) == project_id, col(Collection.id) == id))
            .returning(col(Collection.id))
        )
        result = await self.session.execute(statement)
        deleted_id = result.fetchone()
        await self.session.commit()
        return deleted_id is not None
