# Open Responses 2026 — Implementation Plan

## Stack
- **LLM**: Pydantic AI (OpenRouter provider, OpenAI-compatible API)
- **Persistence**: SQLModel tables via Alembic (consistent with existing code)
- **Orchestration**: DBOS workflows for reliable LLM calls + retries
- **No auth** (for now)

## Endpoints

| Endpoint | Method | Purpose |
|---|---|---|
| `POST /v1/responses` | HTTP | Create a response (sync or SSE stream) |
| `POST /v1/responses/compact` | HTTP | Compact conversation context |
| `WS /v1/responses` | WebSocket | Persistent connection for multi-turn |
| `POST /v1/conversations` | HTTP | Create a conversation |
| `GET /v1/conversations` | HTTP | List conversations |
| `GET /v1/conversations/{id}` | HTTP | Get conversation with responses |
| `PATCH /v1/conversations/{id}` | HTTP | Update conversation (title, metadata) |
| `DELETE /v1/conversations/{id}` | HTTP | Delete conversation |

## Files to Create

All under `src-fastapi/app/responses/`:

```
app/responses/
  __init__.py
  router.py              # POST /v1/responses, POST /v1/responses/compact, WS /v1/responses
  schemas.py             # All Open Responses Pydantic models
  models.py              # SQLModel tables: Conversation, Response, ResponseItem
  constants.py           # Enums, limits, defaults
  service.py             # Business logic: LLM dispatch, state machine, streaming
  streaming.py           # SSE event builders
  llm.py                 # Pydantic AI Agent wrapper → OpenRouter
  workflow.py            # DBOS workflows for reliable LLM orchestration
  websocket.py           # WebSocket handler
  conversations/
    __init__.py
    router.py            # CRUD for conversations
    schemas.py           # ConversationCreate, ConversationRead, ConversationUpdate
    service.py           # Conversation service
```

## Architecture Flow

```
POST /v1/responses
  → Router
    → ResponseService.create_response()
      → DBOS workflow (reliable, retry on failure)
        → LLM service (Pydantic AI Agent → OpenRouter)
          → Map OR Items → provider-native messages
          → Call OpenRouter API
          → Map response → OR Items
      → Store in DB (if store=True)
      → Return Response object (sync) or SSE stream
```

## 1. Schemas (`schemas.py`)

### Item Types (discriminated union on `type`)

**Input items:**
- `UserMessageItemParam` — `type: "message"`, `role: "user"`, `content: string | ContentPart[]`
- `SystemMessageItemParam` — `type: "message"`, `role: "system"`
- `DeveloperMessageItemParam` — `type: "message"`, `role: "developer"`
- `AssistantMessageItemParam` — `type: "message"`, `role: "assistant"`
- `FunctionCallItemParam` — `type: "function_call"`, `call_id`, `name`, `arguments`
- `FunctionCallOutputItemParam` — `type: "function_call_output"`, `call_id`, `output`
- `ItemReferenceParam` — `type: "item_reference"`, `id`
- `ReasoningItemParam` — `type: "reasoning"`, `summary`
- `CompactionSummaryItemParam` — `type: "compaction"`, `encrypted_content`

**Output items:**
- `Message` — `type: "message"`, `role: "assistant"`, `content: OutputTextContent[]`
- `FunctionCall` — `type: "function_call"`, `call_id`, `name`, `arguments`
- `FunctionCallOutput` — `type: "function_call_output"`, `call_id`, `output`
- `ReasoningBody` — `type: "reasoning"`, `summary`
- `CompactionBody` — `type: "compaction"`, `encrypted_content`

### Content Parts
- `InputTextContentParam` — `type: "input_text"`, `text`
- `InputImageContentParamAutoParam` — `type: "input_image"`, `image_url`, `detail`
- `InputFileContentParam` — `type: "input_file"`, `filename`, `file_data`, `file_url`
- `OutputTextContentParam` — `type: "output_text"`, `text`, `annotations`
- `RefusalContentParam` — `type: "refusal"`, `refusal`

### Response Object
```
ResponseResource {
  id: str (prefix "resp_")
  object: "response"
  created_at: int (unix ts)
  completed_at: int | None
  status: "in_progress" | "completed" | "failed" | "incomplete"
  incomplete_details: {"reason": str} | None
  model: str
  previous_response_id: str | None
  instructions: str | None
  output: ItemField[]
  error: Error | None
  tools: Tool[]
  tool_choice: ...
  truncation: "auto" | "disabled"
  parallel_tool_calls: bool
  text: {"format": ...}
  temperature: number | None
  top_p: number | None
  max_output_tokens: int | None
  max_tool_calls: int | None
  usage: {"input_tokens": int, "output_tokens": int, "total_tokens": int, ...}
  store: bool
  metadata: dict | None
}
```

### Error Schema
```
ErrorBody {
  error: {
    message: str
    type: "server_error" | "invalid_request" | "not_found" | "model_error" | "too_many_requests"
    code: str | None
    param: str | None
  }
}
```

### Streaming Events (Pydantic models)
- `ResponseInProgressEvent`
- `ResponseCompletedEvent`
- `ResponseFailedEvent`
- `ResponseIncompleteEvent`
- `ResponseOutputItemAddedEvent`
- `ResponseOutputItemDoneEvent`
- `ResponseContentPartAddedEvent`
- `ResponseContentPartDoneEvent`
- `ResponseOutputTextDeltaEvent`
- `ResponseOutputTextDoneEvent`
- `ResponseFunctionCallArgumentsDeltaEvent`
- `ResponseFunctionCallArgumentsDoneEvent`

### Request Bodies
- `CreateResponseBody` — full spec (model, input, tools, tool_choice, stream, ...)
- `CompactRequestBody` — model, input, previous_response_id, instructions

## 2. Database Models (`models.py`)

### `Conversation` (SQLModel table: `response_conversations`)
| Column | Type | Notes |
|---|---|---|
| id | str PK | prefixed `conv_` |
| project_id | int FK→projects.id | nullable |
| title | str | |
| metadata | dict | JSONB, nullable |
| created_at | datetime | |
| updated_at | datetime | |

### `Response` (SQLModel table: `responses`)
| Column | Type | Notes |
|---|---|---|
| id | str PK | prefixed `resp_` |
| conversation_id | str FK→conversations.id | |
| previous_response_id | str | nullable |
| model | str | |
| status | str | queued/in_progress/completed/failed/incomplete |
| input_items | list[dict] | JSONB |
| output_items | list[dict] | JSONB, nullable |
| instructions | str | nullable |
| temperature | float | nullable |
| top_p | float | nullable |
| max_output_tokens | int | nullable |
| tools | list[dict] | JSONB, nullable |
| tool_choice | str/dict | nullable |
| usage_prompt_tokens | int | default 0 |
| usage_completion_tokens | int | default 0 |
| usage_total_tokens | int | default 0 |
| error_code | str | nullable |
| error_message | str | nullable |
| duration_ms | int | nullable |
| store | bool | default true |
| created_at | datetime | |
| completed_at | datetime | nullable |
| updated_at | datetime | |

## 3. LLM Layer (`llm.py`)

Use Pydantic AI to talk to OpenRouter:

```python
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel

model = OpenAIModel(
    "openrouter-model-name",
    base_url="https://openrouter.ai/api/v1",
    api_key=settings.openrouter_api_key,
)
agent = Agent(model)
```

The LLM service:
- Maps Open Responses items → Pydantic AI message history
- Calls agent with tools if provided
- Maps response back → Open Responses output items
- Supports streaming via `agent.run_stream()`

## 4. DBOS Workflow (`workflow.py`)

```python
from dbos import DBOS

@DBOS.workflow()
async def create_response_workflow(request: CreateResponseBody) -> ResponseResource:
    # 1. Validate and parse input items
    # 2. Look up previous_response_id if provided
    # 3. Build message history from items
    # 4. Call LLM via Pydantic AI (with retries)
    # 5. Process tool calls (if any)
    # 6. Build ResponseResource output
    # 7. Store in DB if store=True
    # 8. Return response
```

DBOS provides:
- Automatic retries on LLM failures
- Reliable state tracking
- Workflow replay for recovery after crash

## 5. Service (`service.py`)

```python
class ResponseService:
    async def create_response(
        self, body: CreateResponseBody
    ) -> ResponseResource | StreamingResponse:
        # If stream=True → return SSE StreamingResponse
        # If stream=False → return ResponseResource JSON
        # Use DBOS workflow for reliable execution
```

For streaming, the service returns a `StreamingResponse` with `text/event-stream` content type. The streaming generator:
1. Initializes DBOS workflow context
2. Calls Pydantic AI's streaming API
3. Translates chunks to OR streaming events
4. Yields SSE-formatted strings
5. Sends terminal `[DONE]`

## 6. Streaming (`streaming.py`)

Helper functions for SSE event building:

```python
def sse_encode(event_type: str, data: dict) -> str:
    return f"event: {event_type}\ndata: {json.dumps(data)}\n\n"
```

Event lifecycle per spec:
1. `response.in_progress`
2. `response.output_item.added` {item: message with empty content}
3. `response.content_part.added` {part: output_text with ""}
4. `response.output_text.delta` {delta: "..."} (repeated)
5. `response.output_text.done` {text: "..."}
6. `response.content_part.done` {part: ...}
7. `response.output_item.done` {item: full message}
8. `response.completed` (or `response.failed` / `response.incomplete`)
9. `[DONE]` (literal string)

## 7. Router (`router.py`)

```python
router = APIRouter(prefix="/v1", tags=["responses"])

@router.post("/responses")
async def create_response(body: CreateResponseBody, ...):
    """Create a response (sync or SSE stream)."""

@router.post("/responses/compact")
async def compact_response(body: CompactRequestBody, ...):
    """Compact conversation context."""

@router.websocket("/responses")
async def responses_websocket(websocket: WebSocket):
    """WebSocket handler for persistent response creation."""
```

## 8. Conversations Router (`conversations/router.py`)

```python
router = APIRouter(prefix="/v1/conversations", tags=["conversations"])

@router.post("/")           # Create conversation
@router.get("/")            # List conversations
@router.get("/{id}")        # Get conversation + responses
@router.patch("/{id}")      # Update conversation
@router.delete("/{id}")     # Delete conversation
```

## 9. WebSocket (`websocket.py`)

- Accept `type: "response.create"` JSON messages
- Connection-local cache for `store=false` continuation
- Sequential processing of messages
- Send streaming events as WebSocket text messages
- Error envelope: `{type: "error", status: 4xx, error: {code, message}}`
- 60-minute connection limit

## 10. Config Updates (`config.py`)

Add to `Settings`:
```python
openrouter_api_key: str = ""
openrouter_base_url: str = "https://openrouter.ai/api/v1"
openrouter_default_model: str = "deepseek/deepseek-chat"
response_store_enabled: bool = True
```

## 11. Dependencies (`pyproject.toml`)

Already present: `dbos`, `pydantic-ai`, `httpx`, `pydantic`, `sqlmodel`, `fastapi[standard]`

No new deps needed.

## 12. Tests (`tests/test_responses_api.py`)

- `test_basic_text_response` — POST /v1/responses with user message
- `test_streaming_response` — POST /v1/responses?stream=true
- `test_system_prompt` — system role in input
- `test_tool_calling` — define function tool, verify function_call output
- `test_multi_turn` — assistant + user history + previous_response_id
- `test_conversations_crud` — full CRUD cycle for /v1/conversations
- `test_missing_model` — 422 on missing model
- `test_compaction` — POST /v1/responses/compact
- `test_websocket_response` — WS create + events

## Implementation Order

1. **Config** — update `config.py` with OpenRouter settings
2. **Constants + Schemas** — `constants.py`, `schemas.py`
3. **Database Models** — `models.py` + Alembic migration
4. **LLM Layer** — `llm.py` (Pydantic AI Agent → OpenRouter)
5. **Streaming** — `streaming.py` (SSE event builders)
6. **DBOS Workflow** — `workflow.py`
7. **Service** — `service.py`
8. **Router** — `router.py` (REST + WebSocket)
9. **Conversations** — `conversations/` sub-module
10. **Wire into main.py**
11. **Tests** — comprehensive test suite