import os
from enum import Enum
from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI(
    title="Geon AI Backend",
    description="AI-powered assistant for the Geon mapping & GIS application.",
    version="0.1.0",
)

# Allow the Tauri/Vite frontend to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your Tauri app's origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ──────────────────────────────────────────────
# Schemas — Chat
# ──────────────────────────────────────────────

class Role(str, Enum):
    system = "system"
    user = "user"
    assistant = "assistant"


class ChatMessage(BaseModel):
    """A single message in the conversation history."""
    role: Role
    content: str


class ChatRequest(BaseModel):
    """The payload the frontend sends to /api/chat."""
    messages: list[ChatMessage] = Field(
        ..., description="Ordered conversation history."
    )


class ChatResponse(BaseModel):
    """Non-streaming response shape (for reference/testing)."""
    role: Role = Role.assistant
    content: str


# ──────────────────────────────────────────────
# Schemas — Tool Calling / Map Actions
# ──────────────────────────────────────────────

class MapActionType(str, Enum):
    """The set of actions the AI can trigger on the map."""
    generate_flood_zone = "generate_flood_zone"
    generate_shelter = "generate_shelter"
    find_underserved_areas = "find_underserved_areas"


class MapActionParams(BaseModel):
    """Parameters the AI provides when it invokes a map tool."""
    location: Optional[str] = Field(
        None, description="Target location name or coordinates."
    )
    radius_km: Optional[float] = Field(
        None, description="Radius in kilometres for spatial queries."
    )
    travel_time_minutes: Optional[int] = Field(
        None, description="Max travel time constraint (walking)."
    )


class MapAction(BaseModel):
    """A tool-call the AI wants the frontend to execute."""
    action: MapActionType
    params: MapActionParams = Field(default_factory=MapActionParams)


# ──────────────────────────────────────────────
# Endpoints
# ──────────────────────────────────────────────

@app.post("/api/chat")
async def chat(request: ChatRequest):
    """
    Accepts conversation history and returns a streamed response.

    Currently returns a mock echo. When the API key is ready,
    replace the generator below with a real OpenAI streaming call.
    """
    last_user_msg = next(
        (m.content for m in reversed(request.messages) if m.role == Role.user),
        "",
    )

    async def generate():
        # TODO: Replace with real OpenAI streaming call
        mock_reply = (
            f"[Mock] I received your message: \"{last_user_msg}\". "
            "Once the API key is configured, I will provide a real AI response."
        )
        for word in mock_reply.split(" "):
            yield word + " "

    return StreamingResponse(generate(), media_type="text/plain")


@app.get("/")
async def root():
    return {"status": "ok", "message": "Geon AI Backend is running!"}
