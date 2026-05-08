from typing import NoReturn

from fastapi import HTTPException, status

from app.conversations.models import Conversation
from app.conversations.repository import ConversationRepository
from app.conversations.schemas import ConversationCreate, ConversationUpdate, ConversationWithResponses
from app.responses.service import ResponseService


class ConversationService:
    def __init__(self, repository: ConversationRepository) -> None:
        self.repository = repository

    async def create(self, conversation: ConversationCreate) -> Conversation:
        return await self.repository.create(conversation)

    async def list_all(self) -> list[Conversation]:
        return await self.repository.list_all()

    async def get(self, conversation_id: str) -> Conversation:
        conv = await self.repository.get(conversation_id)
        if conv is None:
            raise_conversation_not_found(conversation_id)
        return conv

    async def get_with_responses(
        self, conversation_id: str, response_service: ResponseService
    ) -> ConversationWithResponses:
        conv = await self.repository.get(conversation_id)
        if conv is None:
            raise_conversation_not_found(conversation_id)
        responses = await response_service.list_by_conversation(conversation_id)
        return ConversationWithResponses(
            id=conv.id,
            project_id=conv.project_id,
            title=conv.title,
            metadata=conv.metadata_,
            created_at=conv.created_at,
            updated_at=conv.updated_at,
            responses=responses,
        )

    async def update(self, conversation_id: str, conversation: ConversationUpdate) -> Conversation:
        updated = await self.repository.update(conversation_id, conversation)
        if updated is None:
            raise_conversation_not_found(conversation_id)
        return updated

    async def delete(self, conversation_id: str) -> None:
        if not await self.repository.delete(conversation_id):
            raise_conversation_not_found(conversation_id)


def raise_conversation_not_found(identifier: str) -> NoReturn:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"message": "Conversation not found", "identifier": identifier},
    )