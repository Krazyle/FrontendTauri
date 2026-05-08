import pytest
import httpx
from httpx import AsyncClient, ASGITransport
from main import app
from unittest.mock import patch, AsyncMock, MagicMock


@pytest.mark.asyncio
async def test_proxy_functions_forwarding():
    mock_response = httpx.Response(
        200,
        content=b'{"functions": []}',
        headers={"Content-Type": "application/json"},
    )

    with patch("app.proxy.service.httpx.AsyncClient") as mock_client_class:
        mock_client = MagicMock()
        mock_client.get = AsyncMock(return_value=mock_response)
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_client_class.return_value = mock_client

        async with AsyncClient(
            transport=ASGITransport(app=app, raise_app_exceptions=False),
            base_url="http://test",
        ) as ac:
            headers = {"Accept": "application/geo+json"}
            response = await ac.get("/projects/1/functions", headers=headers)

        assert response.status_code == 200
        assert response.json() == {"functions": []}

        args, kwargs = mock_client.get.call_args
        forwarded_headers = {k.lower(): v for k, v in kwargs["headers"].items()}
        assert forwarded_headers["accept"] == "application/geo+json"
        assert "host" not in forwarded_headers


@pytest.mark.asyncio
async def test_proxy_function_detail_forwarding():
    mock_response = httpx.Response(
        200,
        content=b'{"functions": [{"id": "fn1"}]}',
        headers={"Content-Type": "application/json"},
    )

    with patch("app.proxy.service.httpx.AsyncClient") as mock_client_class:
        mock_client = MagicMock()
        mock_client.get = AsyncMock(return_value=mock_response)
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_client_class.return_value = mock_client

        async with AsyncClient(
            transport=ASGITransport(app=app, raise_app_exceptions=False),
            base_url="http://test",
        ) as ac:
            response = await ac.get("/projects/1/functions/summary")

        assert response.status_code == 200
        assert mock_client.get.called
        assert "functions/summary" in mock_client.get.call_args[0][0]


@pytest.mark.asyncio
async def test_proxy_error_handling():
    with patch("app.proxy.service.httpx.AsyncClient") as mock_client_class:
        mock_client = MagicMock()
        mock_client.get = AsyncMock(side_effect=httpx.ConnectError("Connection refused"))
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_client_class.return_value = mock_client

        async with AsyncClient(
            transport=ASGITransport(app=app, raise_app_exceptions=False),
            base_url="http://test",
        ) as ac:
            response = await ac.get("/projects/1/functions")

        assert response.status_code == 502
        assert "Proxy error" in response.text
