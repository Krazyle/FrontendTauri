from __future__ import annotations

from datetime import datetime
from typing import Annotated, Any
from pydantic import BaseModel, ConfigDict, Field, StringConstraints

from app.responses.constants import (
    CALL_ID_MAX_LENGTH,
    CONTENT_TEXT_MAX_LENGTH,
    ITEM_ID_MAX_LENGTH,
    MODEL_MAX_LENGTH,
    TOOL_NAME_MAX_LENGTH,
    AssistantPhase,
    ItemStatus,
    MessageRole,
    ResponseStatus,
    ServiceTier,
    StreamingEventType,
    ToolChoiceValue,
    Truncation,
)


# ── String constraints ──────────────────────────────────────────────────

ModelName = Annotated[str, StringConstraints(max_length=MODEL_MAX_LENGTH, min_length=1)]
ItemId = Annotated[str, StringConstraints(max_length=ITEM_ID_MAX_LENGTH)]
CallId = Annotated[str, StringConstraints(max_length=CALL_ID_MAX_LENGTH)]
ToolName = Annotated[
    str, StringConstraints(max_length=TOOL_NAME_MAX_LENGTH, pattern=r"^[a-zA-Z0-9_-]+$")
]


# ── Error ───────────────────────────────────────────────────────────────


class ErrorBody(BaseModel):
    message: str
    type: str = "invalid_request"
    code: str | None = None
    param: str | None = None


class ErrorEnvelope(BaseModel):
    error: ErrorBody


# ── Content parts ───────────────────────────────────────────────────────


class InputTextContentParam(BaseModel):
    type: str = "input_text"
    text: Annotated[str, StringConstraints(max_length=CONTENT_TEXT_MAX_LENGTH)]


class InputImageContentParam(BaseModel):
    type: str = "input_image"
    image_url: str | None = None
    detail: str | None = None


class InputFileContentParam(BaseModel):
    type: str = "input_file"
    filename: str | None = None
    file_data: str | None = None
    file_url: str | None = None


class OutputTextContentParam(BaseModel):
    type: str = "output_text"
    text: str = ""
    annotations: list[dict] = Field(default_factory=list)


class RefusalContentParam(BaseModel):
    type: str = "refusal"
    refusal: str


# ── Input Items ─────────────────────────────────────────────────────────


class UserMessageItemParam(BaseModel):
    type: str = "message"
    role: str = "user"
    content: str | list[InputTextContentParam | InputImageContentParam | InputFileContentParam]
    id: str | None = None
    status: str | None = None


class SystemMessageItemParam(BaseModel):
    type: str = "message"
    role: str = "system"
    content: str | list[InputTextContentParam]
    id: str | None = None
    status: str | None = None


class DeveloperMessageItemParam(BaseModel):
    type: str = "message"
    role: str = "developer"
    content: str | list[InputTextContentParam]
    id: str | None = None
    status: str | None = None


class AssistantMessageItemParam(BaseModel):
    type: str = "message"
    role: str = "assistant"
    content: str | list[OutputTextContentParam | RefusalContentParam]
    id: str | None = None
    status: str | None = None
    phase: AssistantPhase | None = None


class FunctionCallItemParam(BaseModel):
    type: str = "function_call"
    call_id: CallId
    name: ToolName
    arguments: str
    id: str | None = None
    status: ItemStatus | None = None


class ItemReferenceParam(BaseModel):
    type: str = "item_reference"
    id: ItemId


ItemParam = (
    UserMessageItemParam
    | SystemMessageItemParam
    | DeveloperMessageItemParam
    | AssistantMessageItemParam
    | FunctionCallItemParam
    | ItemReferenceParam
)


# ── Output Items ────────────────────────────────────────────────────────


class Message(BaseModel):
    type: str = "message"
    id: str
    status: ItemStatus = ItemStatus.COMPLETED
    role: MessageRole = MessageRole.ASSISTANT
    content: list[OutputTextContentParam | RefusalContentParam] = Field(default_factory=list)


class FunctionCall(BaseModel):
    type: str = "function_call"
    id: str
    call_id: str
    name: str
    arguments: str
    status: ItemStatus = ItemStatus.COMPLETED


class FunctionCallOutput(BaseModel):
    type: str = "function_call_output"
    id: str
    call_id: str
    output: str
    status: ItemStatus = ItemStatus.COMPLETED


ItemField = Message | FunctionCall | FunctionCallOutput


# ── Tools ───────────────────────────────────────────────────────────────


class FunctionToolParam(BaseModel):
    type: str = "function"
    name: ToolName
    description: str | None = None
    parameters: dict[str, Any] | None = None
    strict: bool = True


class SpecificFunctionParam(BaseModel):
    type: str = "function"
    name: str


# ── Request ─────────────────────────────────────────────────────────────


class StreamOptionsParam(BaseModel):
    include_obfuscation: bool | None = None


class CreateResponseBody(BaseModel):
    model: str = ""
    input: str | list[ItemParam] | None = None
    previous_response_id: str | None = None
    instructions: str | None = None
    store: bool = True
    stream: bool = False
    stream_options: StreamOptionsParam | None = None
    temperature: float | None = None
    top_p: float | None = None
    max_output_tokens: int | None = None
    tools: list[FunctionToolParam] | None = None
    tool_choice: ToolChoiceValue | SpecificFunctionParam | None = None
    metadata: dict[str, str] | None = None
    reasoning: dict[str, Any] | None = None
    truncation: Truncation = Truncation.AUTO
    service_tier: ServiceTier = ServiceTier.AUTO
    frequency_penalty: float | None = None
    presence_penalty: float | None = None
    parallel_tool_calls: bool | None = None
    max_tool_calls: int | None = None
    top_logprobs: int | None = None


# ── Usage ───────────────────────────────────────────────────────────────


class InputTokensDetails(BaseModel):
    cached_tokens: int = 0


class OutputTokensDetails(BaseModel):
    reasoning_tokens: int = 0


class Usage(BaseModel):
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    input_tokens_details: InputTokensDetails = Field(default_factory=InputTokensDetails)
    output_tokens_details: OutputTokensDetails = Field(default_factory=OutputTokensDetails)


# ── Response ────────────────────────────────────────────────────────────


class IncompleteDetails(BaseModel):
    reason: str


class ResponseResource(BaseModel):
    id: str
    object: str = "response"
    created_at: int
    completed_at: int | None = None
    status: ResponseStatus = ResponseStatus.COMPLETED
    incomplete_details: IncompleteDetails | None = None
    model: str
    previous_response_id: str | None = None
    instructions: str | None = None
    output: list[ItemField] = Field(default_factory=list)
    error: ErrorBody | None = None
    tools: list[FunctionToolParam] = Field(default_factory=list)
    tool_choice: ToolChoiceValue | SpecificFunctionParam | None = None
    truncation: Truncation = Truncation.AUTO
    parallel_tool_calls: bool = True
    text: dict[str, Any] = Field(default_factory=dict)
    temperature: float | None = None
    top_p: float | None = None
    max_output_tokens: int | None = None
    max_tool_calls: int | None = None
    usage: Usage = Field(default_factory=Usage)
    store: bool = True
    metadata: dict[str, str] = Field(default_factory=dict)
    service_tier: ServiceTier = ServiceTier.AUTO


# ── Streaming Events ────────────────────────────────────────────────────


class BaseStreamingEvent(BaseModel):
    type: str
    sequence_number: int = 0


class ResponseInProgressEvent(BaseStreamingEvent):
    type: str = StreamingEventType.RESPONSE_IN_PROGRESS
    response: dict[str, Any]


class ResponseCompletedEvent(BaseStreamingEvent):
    type: str = StreamingEventType.RESPONSE_COMPLETED
    response: dict[str, Any]


class ResponseFailedEvent(BaseStreamingEvent):
    type: str = StreamingEventType.RESPONSE_FAILED
    error: ErrorBody


class ResponseIncompleteEvent(BaseStreamingEvent):
    type: str = StreamingEventType.RESPONSE_INCOMPLETE
    incomplete_details: IncompleteDetails


class ResponseOutputItemAddedEvent(BaseStreamingEvent):
    type: str = StreamingEventType.RESPONSE_OUTPUT_ITEM_ADDED
    output_index: int
    item: ItemField


class ResponseOutputItemDoneEvent(BaseStreamingEvent):
    type: str = StreamingEventType.RESPONSE_OUTPUT_ITEM_DONE
    output_index: int
    item: ItemField


class ResponseContentPartAddedEvent(BaseStreamingEvent):
    type: str = StreamingEventType.RESPONSE_CONTENT_PART_ADDED
    item_id: str
    output_index: int
    content_index: int
    part: OutputTextContentParam | RefusalContentParam


class ResponseContentPartDoneEvent(BaseStreamingEvent):
    type: str = StreamingEventType.RESPONSE_CONTENT_PART_DONE
    item_id: str
    output_index: int
    content_index: int
    part: OutputTextContentParam | RefusalContentParam


class ResponseOutputTextDeltaEvent(BaseStreamingEvent):
    type: str = StreamingEventType.RESPONSE_OUTPUT_TEXT_DELTA
    item_id: str
    output_index: int
    content_index: int
    delta: str


class ResponseOutputTextDoneEvent(BaseStreamingEvent):
    type: str = StreamingEventType.RESPONSE_OUTPUT_TEXT_DONE
    item_id: str
    output_index: int
    content_index: int
    text: str


# ── Response Read Schema ──────────────────────────────────────────────


class ResponseRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    conversation_id: str
    previous_response_id: str | None = None
    model: str
    status: str
    instructions: str | None = None
    input_items: list[dict[str, Any]] = Field(default_factory=list)
    output_items: list[dict[str, Any]] = Field(default_factory=list)
    usage_prompt_tokens: int = 0
    usage_completion_tokens: int = 0
    usage_total_tokens: int = 0
    error_code: str | None = None
    error_message: str | None = None
    store: bool = True
    created_at: datetime
    completed_at: datetime | None = None
    updated_at: datetime
