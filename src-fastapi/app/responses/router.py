from __future__ import annotations

from collections.abc import AsyncIterator

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import StreamingResponse

from app.responses.dependencies import ResponseServiceDependency
from app.responses.constants import ErrorType
from app.responses.schemas import CreateResponseBody, ErrorBody, ErrorEnvelope, ResponseResource

router = APIRouter(prefix="/v1", tags=["responses"])


@router.post("/responses", response_model=None, status_code=status.HTTP_200_OK)
async def create_response(
    body: CreateResponseBody,
    service: ResponseServiceDependency,
) -> ResponseResource | StreamingResponse:
    try:
        if body.stream:
            return StreamingResponse(
                _stream_response(service, body),
                media_type="text/event-stream",
                headers={
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                    "X-Accel-Buffering": "no",
                },
            )
        return await service.create(body)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorEnvelope(
                error=ErrorBody(
                    message=str(exc),
                    type=ErrorType.SERVER_ERROR,
                )
            ).model_dump(),
        )


async def _stream_response(
    service: ResponseServiceDependency,
    body: CreateResponseBody,
) -> AsyncIterator[str]:
    try:
        async for event in service.create_stream(body):
            yield event
    except Exception as exc:
        error_event = ErrorEnvelope(
            error=ErrorBody(
                message=str(exc),
                type=ErrorType.SERVER_ERROR,
                code="stream_error",
            )
        )
        yield f"event: response.failed\ndata: {error_event.model_dump_json()}\n\n"
        yield "[DONE]"