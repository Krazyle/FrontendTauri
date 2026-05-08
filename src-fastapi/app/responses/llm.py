from __future__ import annotations

from collections.abc import AsyncIterator

from pydantic_ai import Agent
from pydantic_ai.messages import ModelMessage, ModelRequest, ModelResponse, TextPart, UserPromptPart
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

from config import get_settings

from app.responses.schemas import (
    AssistantMessageItemParam,
    CreateResponseBody,
    DeveloperMessageItemParam,
    ItemParam,
    SystemMessageItemParam,
    UserMessageItemParam,
)


class LLMService:
    def __init__(self) -> None:
        settings = get_settings()
        provider = OpenAIProvider(
            base_url=settings.openrouter_base_url,
            api_key=settings.openrouter_api_key,
        )
        model = OpenAIChatModel(
            settings.openrouter_default_model,
            provider=provider,
        )
        self._agent: Agent[None] = Agent(model)
        self._model_name = settings.openrouter_default_model

    @property
    def model_name(self) -> str:
        return self._model_name

    async def generate(
        self,
        body: CreateResponseBody,
    ) -> tuple[str, int, int]:
        messages = _build_messages(body.input or [])
        result = await self._agent.run(
            messages,
            model_settings={"max_tokens": body.max_output_tokens}
            if body.max_output_tokens
            else None,
        )
        text = result.data
        usage = result.usage()
        return text, usage.request_tokens or 0, usage.response_tokens or 0

    async def generate_stream(
        self,
        body: CreateResponseBody,
    ) -> AsyncIterator[str]:
        messages = _build_messages(body.input or [])
        async with self._agent.run_stream(
            messages,
            model_settings={"max_tokens": body.max_output_tokens}
            if body.max_output_tokens
            else None,
        ) as result:
            async for chunk in result.stream(debounce_by=0.0):
                yield chunk


def _build_messages(input_items: list[ItemParam] | str) -> list[ModelMessage]:
    if isinstance(input_items, str):
        return [ModelRequest(parts=[UserPromptPart(content=input_items)])]

    messages: list[ModelMessage] = []
    for item in input_items:
        if isinstance(item, UserMessageItemParam):
            text = _extract_text_content(item.content)
            messages.append(ModelRequest(parts=[UserPromptPart(content=text)]))
        elif isinstance(item, SystemMessageItemParam | DeveloperMessageItemParam):
            text = _extract_text_content(item.content)
            messages.append(ModelRequest(parts=[UserPromptPart(content=text)]))
        elif isinstance(item, AssistantMessageItemParam):
            text = _extract_text_content(item.content)
            messages.append(ModelResponse(parts=[TextPart(content=text)]))
    return messages


def _extract_text_content(
    content: str | list,
) -> str:
    if isinstance(content, str):
        return content
    parts: list[str] = []
    for part in content:
        if hasattr(part, "text") and part.text:
            parts.append(part.text)
    return "\n".join(parts)
