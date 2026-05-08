from __future__ import annotations

import json
from collections.abc import AsyncIterator
from typing import Any

from app.responses.constants import StreamingEventType


def sse_encode(event_type: str, data: dict[str, Any]) -> str:
    return f"event: {event_type}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n"


async def stream_sse_events(
    text_chunks: AsyncIterator[str],
    item_id: str,
    output_index: int = 0,
    content_index: int = 0,
) -> AsyncIterator[str]:
    """Wraps raw text chunks into Open Responses SSE event stream."""
    collected_text = ""

    # 1. Add the output item
    yield sse_encode(
        StreamingEventType.RESPONSE_OUTPUT_ITEM_ADDED,
        {
            "type": StreamingEventType.RESPONSE_OUTPUT_ITEM_ADDED,
            "sequence_number": 0,
            "output_index": output_index,
            "item": {
                "id": item_id,
                "type": "message",
                "status": "in_progress",
                "content": [],
                "role": "assistant",
            },
        },
    )

    # 2. Add content part
    yield sse_encode(
        StreamingEventType.RESPONSE_CONTENT_PART_ADDED,
        {
            "type": StreamingEventType.RESPONSE_CONTENT_PART_ADDED,
            "sequence_number": 1,
            "item_id": item_id,
            "output_index": output_index,
            "content_index": content_index,
            "part": {"type": "output_text", "annotations": [], "text": ""},
        },
    )

    seq = 2
    async for chunk in text_chunks:
        collected_text += chunk
        yield sse_encode(
            StreamingEventType.RESPONSE_OUTPUT_TEXT_DELTA,
            {
                "type": StreamingEventType.RESPONSE_OUTPUT_TEXT_DELTA,
                "sequence_number": seq,
                "item_id": item_id,
                "output_index": output_index,
                "content_index": content_index,
                "delta": chunk,
            },
        )
        seq += 1

    # 3. Done with text
    yield sse_encode(
        StreamingEventType.RESPONSE_OUTPUT_TEXT_DONE,
        {
            "type": StreamingEventType.RESPONSE_OUTPUT_TEXT_DONE,
            "sequence_number": seq,
            "item_id": item_id,
            "output_index": output_index,
            "content_index": content_index,
            "text": collected_text,
        },
    )
    seq += 1

    # 4. Done with content part
    yield sse_encode(
        StreamingEventType.RESPONSE_CONTENT_PART_DONE,
        {
            "type": StreamingEventType.RESPONSE_CONTENT_PART_DONE,
            "sequence_number": seq,
            "item_id": item_id,
            "output_index": output_index,
            "content_index": content_index,
            "part": {
                "type": "output_text",
                "annotations": [],
                "text": collected_text,
            },
        },
    )
    seq += 1

    # 5. Done with output item
    yield sse_encode(
        StreamingEventType.RESPONSE_OUTPUT_ITEM_DONE,
        {
            "type": StreamingEventType.RESPONSE_OUTPUT_ITEM_DONE,
            "sequence_number": seq,
            "output_index": output_index,
            "item": {
                "id": item_id,
                "type": "message",
                "status": "completed",
                "content": [
                    {
                        "type": "output_text",
                        "annotations": [],
                        "text": collected_text,
                    }
                ],
                "role": "assistant",
            },
        },
    )


def sse_response_completed(response_dict: dict[str, Any], seq: int = 0) -> str:
    return sse_encode(
        StreamingEventType.RESPONSE_COMPLETED,
        {
            "type": StreamingEventType.RESPONSE_COMPLETED,
            "sequence_number": seq,
            "response": response_dict,
        },
    )


def sse_response_in_progress(response_dict: dict[str, Any], seq: int = 0) -> str:
    return sse_encode(
        StreamingEventType.RESPONSE_IN_PROGRESS,
        {
            "type": StreamingEventType.RESPONSE_IN_PROGRESS,
            "sequence_number": seq,
            "response": response_dict,
        },
    )


DONE_MARKER = "[DONE]"
