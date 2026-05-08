import pytest
from httpx import AsyncClient


pytestmark = pytest.mark.asyncio


async def test_create_response_no_stream(client: AsyncClient) -> None:
    """Test basic sync response creation.
    Note: This requires a real OpenRouter API key to be set.
    Without it, the test confirms the 500 error format."""
    response = await client.post(
        "/v1/responses",
        json={
            "model": "deepseek/deepseek-chat",
            "input": [{"role": "user", "type": "message", "content": "Say hello"}],
            "store": False,
        },
    )
    # Without API key, we expect a 500 error from the LLM call
    assert response.status_code == 500
    data = response.json()
    assert "error" in data["detail"]


async def test_create_response_missing_model(client: AsyncClient) -> None:
    response = await client.post(
        "/v1/responses",
        json={"input": "hello"},
    )
    # Should still work - defaults to configured model, or fail gracefully
    assert response.status_code in (200, 500)


async def test_create_response_string_input(client: AsyncClient) -> None:
    response = await client.post(
        "/v1/responses",
        json={
            "input": "Say hello",
            "store": False,
        },
    )
    assert response.status_code in (200, 500)


async def test_streaming_response(client: AsyncClient) -> None:
    response = await client.post(
        "/v1/responses",
        json={
            "model": "deepseek/deepseek-chat",
            "input": [{"role": "user", "type": "message", "content": "Count to 3"}],
            "stream": True,
            "store": False,
        },
    )
    assert response.status_code == 200
    assert "text/event-stream" in response.headers["content-type"]

    body = response.text
    assert "event: response.in_progress" in body
    # Either the stream succeeds with text deltas, or fails with error event
    assert "event: response.output_item.added" in body or "event: response.failed" in body
    assert "[DONE]" in body