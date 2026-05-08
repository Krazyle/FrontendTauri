import pytest
import httpx
from httpx import AsyncClient, ASGITransport
from main import app
from unittest.mock import patch, AsyncMock, MagicMock

@pytest.mark.asyncio
async def test_proxy_collections_forwarding():
    mock_response = httpx.Response(
        200, 
        content=b'{"collections": []}', 
        headers={"Content-Type": "application/json"}
    )

    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = mock_response
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            headers = {"Accept": "application/geo+json"}
            response = await ac.get("/collections", headers=headers)

        assert response.status_code == 200
        assert response.json() == {"collections": []}
        
        args, kwargs = mock_get.call_args
        forwarded_headers = {k.lower(): v for k, v in kwargs["headers"].items()}
        assert forwarded_headers["accept"] == "application/geo+json"
        assert "host" not in forwarded_headers

@pytest.mark.asyncio
async def test_proxy_functions_forwarding():
    mock_response = httpx.Response(
        200, 
        content=b'{"functions": []}', 
        headers={"Content-Type": "application/json"}
    )

    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = mock_response
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            response = await ac.get("/functions")

        assert response.status_code == 200
        assert response.json() == {"functions": []}
        assert mock_get.called
        assert "functions" in mock_get.call_args[0][0]

@pytest.mark.asyncio
async def test_proxy_error_handling():
    with patch("app.proxy.router.httpx.AsyncClient") as mock_client_class:
        mock_client = MagicMock()
        mock_client.get = AsyncMock(side_effect=httpx.ConnectError("Connection refused"))
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_client_class.return_value = mock_client

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            response = await ac.get("/collections")

        assert response.status_code == 502
        assert "Proxy error" in response.text
