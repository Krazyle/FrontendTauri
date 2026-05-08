from typing import Annotated

from fastapi import Depends
from database import DatabaseSessionDependency
from app.conversations.repository import ConversationRepository
from app.conversations.service import ConversationService


def get_conversation_repository(session: DatabaseSessionDependency) -> ConversationRepository:
    return ConversationRepository(session)


ConversationRepositoryDependency = Annotated[
    ConversationRepository, Depends(get_conversation_repository)
]


def get_conversation_service(
    repository: ConversationRepositoryDependency,
) -> ConversationService:
    return ConversationService(repository)


ConversationServiceDependency = Annotated[ConversationService, Depends(get_conversation_service)]
