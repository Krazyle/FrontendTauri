import os

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

e2e = pytest.mark.skipif(
    not os.environ.get("OPENROUTER_API_KEY"),
    reason="OPENROUTER_API_KEY not set — skipping end-to-end test",
)


@e2e
async def test_e2e_response_non_streaming(client: AsyncClient) -> None:
    response = await client.post(
        "/v1/responses",
        json={
            "input": [{"role": "user", "type": "message", "content": "Return only the word: hello"}],
            "store": False,
            "max_output_tokens": 50,
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"].startswith("resp_")
    assert data["status"] == "completed"
    assert data["object"] == "response"
    assert len(data["output"]) == 1
    msg = data["output"][0]
    assert msg["role"] == "assistant"
    assert msg["status"] == "completed"
    assert len(msg["content"]) == 1
    assert "hello" in msg["content"][0]["text"].lower()
    assert data["usage"]["input_tokens"] > 0
    assert data["usage"]["output_tokens"] > 0
    assert data["usage"]["total_tokens"] > 0


@e2e
async def test_e2e_response_streaming(client: AsyncClient) -> None:
    response = await client.post(
        "/v1/responses",
        json={
            "input": [{"role": "user", "type": "message", "content": "Return only the word: hello"}],
            "stream": True,
            "store": False,
            "max_output_tokens": 50,
        },
    )
    assert response.status_code == 200
    assert "text/event-stream" in response.headers["content-type"]

    body = response.text
    assert "event: response.in_progress" in body
    assert "event: response.output_item.added" in body
    assert "event: response.content_part.added" in body
    assert "event: response.output_text.delta" in body
    assert "event: response.output_text.done" in body
    assert "event: response.content_part.done" in body
    assert "event: response.output_item.done" in body
    assert "event: response.completed" in body
    assert "[DONE]" in body
    assert "hello" in body.lower()


@e2e
async def test_e2e_conversation_with_stored_response(client: AsyncClient) -> None:
    conv_resp = await client.post("/v1/conversations/", json={"title": "E2E Test Chat"})
    assert conv_resp.status_code == 201
    conv_id = conv_resp.json()["id"]

    resp_resp = await client.post(
        "/v1/responses",
        json={
            "input": [{"role": "user", "type": "message", "content": "Return only: hello world"}],
            "previous_response_id": conv_id,
            "store": True,
            "max_output_tokens": 50,
        },
    )
    assert resp_resp.status_code == 200, resp_resp.text
    resp_data = resp_resp.json()
    response_id = resp_data["id"]

    conv_read = await client.get(f"/v1/conversations/{conv_id}")
    assert conv_read.status_code == 200
    conv_data = conv_read.json()

    assert conv_data["title"] == "E2E Test Chat"
    assert len(conv_data["responses"]) >= 1
    stored = next(r for r in conv_data["responses"] if r["id"] == response_id)
    assert stored["model"] == "deepseek/deepseek-chat"
    assert stored["status"] == "completed"
    assert stored["usage_total_tokens"] > 0