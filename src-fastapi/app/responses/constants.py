from enum import StrEnum

ID_RESPONSE_PREFIX = "resp_"
ID_ITEM_PREFIX = "msg_"
ID_CALL_PREFIX = "call_"

MODEL_MAX_LENGTH = 128
ITEM_ID_MAX_LENGTH = 64
CALL_ID_MAX_LENGTH = 64
TOOL_NAME_MAX_LENGTH = 64
CONTENT_TEXT_MAX_LENGTH = 10_485_760
METADATA_KEYS_MAX = 16
METADATA_KEY_MAX_LENGTH = 64
METADATA_VALUE_MAX_LENGTH = 512
TOOL_MAX_COUNT = 128
TOKEN_MAX = 20
MAX_OUTPUT_TOKENS_MIN = 16


class ResponseStatus(StrEnum):
    QUEUED = "queued"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    INCOMPLETE = "incomplete"


class ItemStatus(StrEnum):
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    INCOMPLETE = "incomplete"


class MessageRole(StrEnum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    DEVELOPER = "developer"


class ItemType(StrEnum):
    MESSAGE = "message"
    FUNCTION_CALL = "function_call"
    FUNCTION_CALL_OUTPUT = "function_call_output"
    ITEM_REFERENCE = "item_reference"
    REASONING = "reasoning"
    COMPACTION = "compaction"


class ContentType(StrEnum):
    INPUT_TEXT = "input_text"
    INPUT_IMAGE = "input_image"
    INPUT_FILE = "input_file"
    OUTPUT_TEXT = "output_text"
    REFUSAL = "refusal"
    SUMMARY_TEXT = "summary_text"


class StreamingEventType(StrEnum):
    RESPONSE_IN_PROGRESS = "response.in_progress"
    RESPONSE_COMPLETED = "response.completed"
    RESPONSE_FAILED = "response.failed"
    RESPONSE_INCOMPLETE = "response.incomplete"
    RESPONSE_OUTPUT_ITEM_ADDED = "response.output_item.added"
    RESPONSE_OUTPUT_ITEM_DONE = "response.output_item.done"
    RESPONSE_CONTENT_PART_ADDED = "response.content_part.added"
    RESPONSE_CONTENT_PART_DONE = "response.content_part.done"
    RESPONSE_OUTPUT_TEXT_DELTA = "response.output_text.delta"
    RESPONSE_OUTPUT_TEXT_DONE = "response.output_text.done"
    RESPONSE_FUNCTION_CALL_ARGUMENTS_DELTA = "response.function_call_arguments.delta"
    RESPONSE_FUNCTION_CALL_ARGUMENTS_DONE = "response.function_call_arguments.done"


class ErrorType(StrEnum):
    SERVER_ERROR = "server_error"
    INVALID_REQUEST = "invalid_request"
    NOT_FOUND = "not_found"
    MODEL_ERROR = "model_error"
    TOO_MANY_REQUESTS = "too_many_requests"


class Truncation(StrEnum):
    AUTO = "auto"
    DISABLED = "disabled"


class ServiceTier(StrEnum):
    AUTO = "auto"
    DEFAULT = "default"
    FLEX = "flex"
    PRIORITY = "priority"


class AssistantPhase(StrEnum):
    COMMENTARY = "commentary"
    FINAL_ANSWER = "final_answer"


class ToolChoiceValue(StrEnum):
    NONE = "none"
    AUTO = "auto"
    REQUIRED = "required"


ERROR_STATUS_MAP: dict[ErrorType, int] = {
    ErrorType.SERVER_ERROR: 500,
    ErrorType.INVALID_REQUEST: 400,
    ErrorType.NOT_FOUND: 404,
    ErrorType.MODEL_ERROR: 500,
    ErrorType.TOO_MANY_REQUESTS: 429,
}
