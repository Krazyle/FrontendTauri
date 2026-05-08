import json
import pytest
from httpx import AsyncClient
from unittest.mock import patch, AsyncMock, MagicMock


pytestmark = pytest.mark.asyncio


async def _create_project_and_collection(client: AsyncClient) -> tuple[int, int]:
    proj_resp = await client.post("/projects/", json={"name": "Items Test"})
    project_id = proj_resp.json()["id"]

    coll_resp = await client.post(
        f"/projects/{project_id}/collections/",
        json={
            "collection_id": "item_tests",
            "title": "Item Tests",
            "table_name": "items_test",
        },
    )
    return project_id, coll_resp.json()["id"]


async def test_list_items_proxies_to_pg_featureserv(client: AsyncClient) -> None:
    project_id, collection_id = await _create_project_and_collection(client)

    proxy_body = {
        "type": "FeatureCollection",
        "features": [],
        "links": [],
    }
    mock_response = MagicMock(status_code=200, body=json.dumps(proxy_body).encode())

    with patch("app.items.router.proxy_request", new_callable=AsyncMock) as mock_proxy:
        mock_proxy.return_value = mock_response
        response = await client.get(f"/projects/{project_id}/collections/{collection_id}/items/")

    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "FeatureCollection"
    assert data["features"] == []


async def test_read_item_proxies_to_pg_featureserv(client: AsyncClient) -> None:
    project_id, collection_id = await _create_project_and_collection(client)

    proxy_body = {
        "type": "Feature",
        "id": 1,
        "geometry": {"type": "Point", "coordinates": [1.0, 2.0]},
        "properties": {},
    }
    mock_response = MagicMock(status_code=200, body=json.dumps(proxy_body).encode())

    with patch("app.items.router.proxy_request", new_callable=AsyncMock) as mock_proxy:
        mock_proxy.return_value = mock_response
        response = await client.get(f"/projects/{project_id}/collections/{collection_id}/items/1")

    assert response.status_code == 200
    assert response.json()["id"] == 1


async def test_create_item(client: AsyncClient) -> None:
    project_id, collection_id = await _create_project_and_collection(client)

    mock_feature = {
        "id": 1,
        "geometry": {"type": "Point", "coordinates": [1.0, 2.0]},
        "properties": {"label": "A"},
        "type": "Feature",
    }

    with patch("app.items.repository.ItemRepository.create", new_callable=AsyncMock) as mock_create:
        mock_create.return_value = mock_feature

        response = await client.post(
            f"/projects/{project_id}/collections/{collection_id}/items/",
            json={
                "geometry": {"type": "Point", "coordinates": [1.0, 2.0]},
                "properties": {"label": "A"},
            },
        )

    assert response.status_code == 201
    body = response.json()
    assert body["id"] == 1
    assert body["geometry"] == {"type": "Point", "coordinates": [1.0, 2.0]}
    assert body["properties"] == {"label": "A"}
    assert body["type"] == "Feature"


async def test_create_item_invalid_geometry(client: AsyncClient) -> None:
    project_id, collection_id = await _create_project_and_collection(client)

    response = await client.post(
        f"/projects/{project_id}/collections/{collection_id}/items/",
        json={
            "geometry": {"type": "InvalidType", "coordinates": [1.0, 2.0]},
            "properties": {},
        },
    )

    assert response.status_code == 422


async def test_update_item(client: AsyncClient) -> None:
    project_id, collection_id = await _create_project_and_collection(client)

    mock_feature = {
        "id": 1,
        "geometry": {"type": "Point", "coordinates": [3.0, 4.0]},
        "properties": {"label": "B"},
        "type": "Feature",
    }

    with patch("app.items.repository.ItemRepository.update", new_callable=AsyncMock) as mock_update:
        mock_update.return_value = mock_feature

        response = await client.patch(
            f"/projects/{project_id}/collections/{collection_id}/items/1",
            json={
                "geometry": {"type": "Point", "coordinates": [3.0, 4.0]},
                "properties": {"label": "B"},
            },
        )

    assert response.status_code == 200
    body = response.json()
    assert body["geometry"]["coordinates"] == [3.0, 4.0]
    assert body["properties"]["label"] == "B"


async def test_delete_item(client: AsyncClient) -> None:
    project_id, collection_id = await _create_project_and_collection(client)

    with patch("app.items.repository.ItemRepository.delete", new_callable=AsyncMock) as mock_delete:
        mock_delete.return_value = True

        response = await client.delete(
            f"/projects/{project_id}/collections/{collection_id}/items/1"
        )

    assert response.status_code == 204
    assert response.content == b""


async def test_delete_item_not_found(client: AsyncClient) -> None:
    project_id, collection_id = await _create_project_and_collection(client)

    with patch("app.items.repository.ItemRepository.delete", new_callable=AsyncMock) as mock_delete:
        mock_delete.return_value = False

        response = await client.delete(
            f"/projects/{project_id}/collections/{collection_id}/items/999"
        )

    assert response.status_code == 404
    assert response.json()["detail"]["message"] == "Item not found"


async def test_create_item_geometry_type_mismatch(client: AsyncClient) -> None:
    project_id, collection_id = await _create_project_and_collection(client)

    # We mock the collection service to return a collection with GeometryType.Point
    from app.collections.constants import GeometryType
    from app.collections.models import Collection

    mock_collection = Collection(
        id=collection_id,
        project_id=project_id,
        collection_id="item_tests",
        title="Item Tests",
        table_name="items_test",
        geometry_type=GeometryType.Point,
    )

    with patch(
        "app.collections.service.CollectionService.get", new_callable=AsyncMock
    ) as mock_get_coll:
        mock_get_coll.return_value = mock_collection

        # Try to create a Polygon in a Point collection
        response = await client.post(
            f"/projects/{project_id}/collections/{collection_id}/items/",
            json={
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[[0, 0], [1, 1], [1, 0], [0, 0]]],
                },
                "properties": {},
            },
        )

    assert response.status_code == 400
    assert response.json()["detail"]["message"] == "Geometry type mismatch"
    assert "only accepts Point geometries" in response.json()["detail"]["reason"]
