from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import col

from app.conversations.models import Conversation
from app.conversations.schemas import ConversationCreate, ConversationUpdate


class ConversationRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, conversation: ConversationCreate) -> Conversation:
        conv = Conversation(
            title=conversation.title,
            project_id=conversation.project_id,
            metadata_=conversation.metadata,
        )
        self.session.add(conv)
        await self.session.commit()
        await self.session.refresh(conv)
        return conv

    async def list_all(self) -> list[Conversation]:
        stmt = select(Conversation).order_by(Conversation.updated_at.desc())
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get(self, conversation_id: str) -> Conversation | None:
        return await self.session.get(Conversation, conversation_id)

    async def update(self, conversation_id: str, conversation: ConversationUpdate) -> Conversation | None:
        conv = await self.get(conversation_id)
        if conv is None:
            return None
        update_data = conversation.model_dump(exclude_unset=True)
        if not update_data:
            return conv
        if "metadata" in update_data:
            conv.metadata_ = update_data.pop("metadata")
        for key, value in update_data.items():
            setattr(conv, key, value)
        await self.session.commit()
        await self.session.refresh(conv)
        return conv

    async def delete(self, conversation_id: str) -> bool:
        stmt = (
            delete(Conversation)
            .where(col(Conversation.id) == conversation_id)
            .returning(col(Conversation.id))
        )
        result = await self.session.execute(stmt)
        deleted_id = result.fetchone()
        await self.session.commit()
        return deleted_id is not None