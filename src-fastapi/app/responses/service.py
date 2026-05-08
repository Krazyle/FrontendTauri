from __future__ import annotations

import re
import secrets
import time
from collections.abc import AsyncIterator

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.responses.constants import (
    ID_ITEM_PREFIX,
    ItemStatus,
    MessageRole,
    ResponseStatus,
)
from app.responses.llm import LLMService
from app.responses.models import Response as ResponseModel
from app.responses.schemas import (
    CreateResponseBody,
    ItemField,
    Message,
    OutputTextContentParam,
    ResponseResource,
    ResponseRead,
    Usage,
)
from app.responses.streaming import (
    DONE_MARKER,
    sse_response_completed,
    sse_response_in_progress,
    stream_sse_events,
)


class ResponseService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self._llm: LLMService | None = None

    @property
    def llm(self) -> LLMService:
        if self._llm is None:
            self._llm = LLMService()
        return self._llm

    async def create(self, body: CreateResponseBody) -> ResponseResource:
        response_id = _generate_item_id()
        start_time = time.monotonic()

        model = body.model or self.llm.model_name
        text, prompt_tokens, completion_tokens = await self.llm.generate(body)

        duration_ms = int((time.monotonic() - start_time) * 1000)

        msg_id = _generate_item_id()
        output_item = Message(
            id=msg_id,
            status=ItemStatus.COMPLETED,
            role=MessageRole.ASSISTANT,
            content=[OutputTextContentParam(text=text)],
        )

        created_at = int(time.time())
        result = ResponseResource(
            id=response_id,
            created_at=created_at,
            completed_at=created_at,
            status=ResponseStatus.COMPLETED,
            model=model,
            instructions=body.instructions,
            output=[output_item],
            usage=Usage(
                input_tokens=prompt_tokens,
                output_tokens=completion_tokens,
                total_tokens=prompt_tokens + completion_tokens,
            ),
            store=body.store,
        )

        if body.store:
            await self._persist(
                body, result, output_item, prompt_tokens, completion_tokens, duration_ms
            )

        return result

    async def create_stream(self, body: CreateResponseBody) -> AsyncIterator[str]:
        response_id = _generate_item_id()
        msg_id = _generate_item_id()

        model = body.model or self.llm.model_name
        created_at = int(time.time())

        response_dict = {
            "id": response_id,
            "object": "response",
            "created_at": created_at,
            "model": model,
            "status": "in_progress",
            "instructions": body.instructions,
            "output": [],
            "usage": {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0},
        }

        initial_dict = dict(response_dict)
        initial_dict["status"] = "in_progress"
        yield sse_response_in_progress(initial_dict)

        text_chunks = self.llm.generate_stream(body)

        collected_text = ""
        async for sse_event in stream_sse_events(text_chunks, msg_id, output_index=0):
            yield sse_event
            if sse_event.startswith("event: response.output_text.delta"):
                m = re.search(r'"delta":"([^"]*)"', sse_event)
                if m:
                    collected_text += m.group(1).encode().decode("unicode_escape")

        output_item = Message(
            id=msg_id,
            status=ItemStatus.COMPLETED,
            role=MessageRole.ASSISTANT,
            content=[OutputTextContentParam(text=collected_text)],
        )

        completed_dict = dict(response_dict)
        completed_dict["status"] = "completed"
        completed_dict["completed_at"] = int(time.time())
        completed_dict["output"] = [output_item.model_dump()]
        yield sse_response_completed(completed_dict)

        yield DONE_MARKER

    async def _persist(
        self,
        body: CreateResponseBody,
        result: ResponseResource,
        output_item: ItemField,
        prompt_tokens: int,
        completion_tokens: int,
        duration_ms: int,
    ) -> None:
        input_items_raw = _serialize_input_items(body.input)
        db_response = ResponseModel(
            id=result.id,
            conversation_id=body.previous_response_id or result.id,
            previous_response_id=body.previous_response_id,
            model=result.model,
            status=result.status,
            instructions=body.instructions,
            input_items=input_items_raw,
            output_items=_serialize_output_items([output_item]),
            usage_prompt_tokens=prompt_tokens,
            usage_completion_tokens=completion_tokens,
            usage_total_tokens=prompt_tokens + completion_tokens,
            duration_ms=duration_ms,
            store=True,
        )
        self.session.add(db_response)
        await self.session.commit()

    async def get_by_id(self, response_id: str) -> ResponseModel | None:
        stmt = select(ResponseModel).where(ResponseModel.id == response_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_conversation(self, conversation_id: str) -> list[ResponseRead]:
        stmt = (
            select(ResponseModel)
            .where(ResponseModel.conversation_id == conversation_id)
            .order_by(ResponseModel.created_at)
        )
        result = await self.session.execute(stmt)
        return [ResponseRead.model_validate(r) for r in result.scalars().all()]


def _generate_item_id() -> str:
    ts = int(time.time() * 1000)
    rand = secrets.token_hex(12)
    return f"{ID_ITEM_PREFIX}{ts:x}{rand[:8]}"


def _serialize_input_items(input_items: str | list | None) -> list[dict] | None:
    if input_items is None:
        return None
    if isinstance(input_items, str):
        return [{"type": "message", "role": "user", "content": input_items}]
    return [
        item.model_dump(exclude_none=True) if hasattr(item, "model_dump") else item
        for item in input_items
    ]


def _serialize_output_items(items: list[ItemField]) -> list[dict]:
    return [item.model_dump() for item in items]