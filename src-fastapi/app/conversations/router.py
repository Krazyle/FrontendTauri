from __future__ import annotations

from fastapi import APIRouter, status

from app.conversations.dependencies import ConversationServiceDependency
from app.conversations.models import Conversation
from app.conversations.schemas import (
    ConversationCreate,
    ConversationRead,
    ConversationUpdate,
    ConversationWithResponses,
)
from app.responses.dependencies import ResponseServiceDependency

router = APIRouter(prefix="/v1/conversations", tags=["conversations"])


def _conv_to_read(conv: Conversation) -> ConversationRead:
    return ConversationRead(
        id=conv.id,
        project_id=conv.project_id,
        title=conv.title,
        metadata=conv.metadata_,
        created_at=conv.created_at,
        updated_at=conv.updated_at,
    )


@router.post("/", response_model=ConversationRead, status_code=status.HTTP_201_CREATED)
async def create_conversation(
    body: ConversationCreate,
    service: ConversationServiceDependency,
) -> ConversationRead:
    return _conv_to_read(await service.create(body))


@router.get("/", response_model=list[ConversationRead], status_code=status.HTTP_200_OK)
async def list_conversations(
    service: ConversationServiceDependency,
) -> list[ConversationRead]:
    return [_conv_to_read(c) for c in await service.list_all()]


@router.get("/{conversation_id}", response_model=ConversationWithResponses, status_code=status.HTTP_200_OK)
async def read_conversation(
    conversation_id: str,
    service: ConversationServiceDependency,
    response_service: ResponseServiceDependency,
) -> ConversationWithResponses:
    return await service.get_with_responses(conversation_id, response_service)


@router.patch("/{conversation_id}", response_model=ConversationRead, status_code=status.HTTP_200_OK)
async def update_conversation(
    conversation_id: str,
    body: ConversationUpdate,
    service: ConversationServiceDependency,
) -> ConversationRead:
    return _conv_to_read(await service.update(conversation_id, body))


@router.delete("/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_conversation(
    conversation_id: str,
    service: ConversationServiceDependency,
) -> None:
    await service.delete(conversation_id)