import json
import pytest
from httpx import AsyncClient
from unittest.mock import patch, AsyncMock, MagicMock


pytestmark = pytest.mark.asyncio


async def test_create_read_list_replace_patch_and_delete_collection(
    client: AsyncClient,
) -> None:
    project_response = await client.post("/projects/", json={"name": "Project 1"})
    project_id = project_response.json()["id"]

    collection_data = {
        "collection_id": "test_collection",
        "title": "Test Collection",
        "description": "A test collection",
        "table_name": "test_table",
    }
    create_response = await client.post(
        f"/projects/{project_id}/collections/",
        json=collection_data,
    )

    assert create_response.status_code == 201
    created_collection = create_response.json()
    assert created_collection["collection_id"] == "test_collection"
    assert created_collection["title"] == "Test Collection"
    assert created_collection["table_name"] == "test_table"
    assert created_collection["status"] == "importing"

    # 3. List collections
    proxy_body = {
        "collections": [{"id": "user_data.test_table"}],
        "links": [],
    }
    mock_response = MagicMock(status_code=200, body=json.dumps(proxy_body).encode())

    with patch("app.collections.router.proxy_request", new_callable=AsyncMock) as mock_proxy:
        mock_proxy.return_value = mock_response
        list_response = await client.get(f"/projects/{project_id}/collections/")

    assert list_response.status_code == 200
    listed = list_response.json()
    assert isinstance(listed, dict)
    assert len(listed["collections"]) == 1
    assert listed["collections"][0]["title"] == "Test Collection"

    # 4. Get specific collection
    proxy_body_get = {"id": "user_data.test_table", "title": "Old Title"}
    mock_response_get = MagicMock(status_code=200, body=json.dumps(proxy_body_get).encode())

    with patch("app.collections.router.proxy_request", new_callable=AsyncMock) as mock_proxy:
        mock_proxy.return_value = mock_response_get
        get_response = await client.get(
            f"/projects/{project_id}/collections/{created_collection['id']}"
        )

    assert get_response.status_code == 200
    assert get_response.json()["title"] == "Test Collection"  # Enriched

    # 5. Replace collection
    replace_data = {
        "collection_id": "test_collection",
        "title": "Replaced Title",
        "description": "Replaced description",
        "table_name": "test_table",
    }
    replace_response = await client.put(
        f"/projects/{project_id}/collections/{created_collection['id']}",
        json=replace_data,
    )
    assert replace_response.status_code == 200
    assert replace_response.json()["title"] == "Replaced Title"
    assert replace_response.json()["description"] == "Replaced description"

    patch_data = {"description": "Patched description"}
    patch_response = await client.patch(
        f"/projects/{project_id}/collections/{created_collection['id']}",
        json=patch_data,
    )
    assert patch_response.status_code == 200
    assert patch_response.json()["title"] == "Replaced Title"
    assert patch_response.json()["description"] == "Patched description"

    delete_response = await client.delete(
        f"/projects/{project_id}/collections/{created_collection['id']}"
    )
    assert delete_response.status_code == 204

    missing_response = await client.get(
        f"/projects/{project_id}/collections/{created_collection['id']}"
    )
    assert missing_response.status_code == 404


async def test_duplicate_collection_id_in_same_project_fails(
    client: AsyncClient,
) -> None:
    project_response = await client.post("/projects/", json={"name": "Project 1"})
    project_id = project_response.json()["id"]

    collection_data = {
        "collection_id": "duplicate",
        "title": "First",
        "table_name": "table_1",
    }
    await client.post(f"/projects/{project_id}/collections/", json=collection_data)

    duplicate_data = {
        "collection_id": "duplicate",
        "title": "Second",
        "table_name": "table_2",
    }
    response = await client.post(f"/projects/{project_id}/collections/", json=duplicate_data)

    assert response.status_code == 409
    assert (
        "A collection with this ID already exists in this project."
        in response.json()["detail"]["reason"]
    )


async def test_duplicate_collection_id_in_different_projects_passes(
    client: AsyncClient,
) -> None:
    p1 = await client.post("/projects/", json={"name": "P1"})
    p2 = await client.post("/projects/", json={"name": "P2"})
    p1_id = p1.json()["id"]
    p2_id = p2.json()["id"]

    data = {
        "collection_id": "shared_id",
        "title": "Title",
        "table_name": "t1",
    }
    await client.post(f"/projects/{p1_id}/collections/", json=data)

    data["table_name"] = "t2"
    response = await client.post(f"/projects/{p2_id}/collections/", json=data)

    assert response.status_code == 201


async def test_duplicate_table_name_fails(client: AsyncClient) -> None:
    p1 = await client.post("/projects/", json={"name": "P1"})
    p1_id = p1.json()["id"]

    await client.post(
        f"/projects/{p1_id}/collections/",
        json={"collection_id": "c1", "title": "C1", "table_name": "shared_table"},
    )

    response = await client.post(
        f"/projects/{p1_id}/collections/",
        json={"collection_id": "c2", "title": "C2", "table_name": "shared_table"},
    )

    assert response.status_code == 409


async def test_invalid_collection_id_fails(client: AsyncClient) -> None:
    project_response = await client.post("/projects/", json={"name": "P1"})
    project_id = project_response.json()["id"]

    response = await client.post(
        f"/projects/{project_id}/collections/",
        json={"collection_id": "1test", "title": "T", "table_name": "t"},
    )
    assert response.status_code == 422

    response = await client.post(
        f"/projects/{project_id}/collections/",
        json={"collection_id": "Test", "title": "T", "table_name": "t"},
    )
    assert response.status_code == 422


async def test_invalid_title_fails(client: AsyncClient) -> None:
    project_response = await client.post("/projects/", json={"name": "P1"})
    project_id = project_response.json()["id"]

    response = await client.post(
        f"/projects/{project_id}/collections/",
        json={"collection_id": "test", "title": "  ", "table_name": "t"},
    )
    assert response.status_code == 422


async def test_collection_read_structured_extent(client: AsyncClient) -> None:
    project_response = await client.post("/projects/", json={"name": "P1"})
    project_id = project_response.json()["id"]

    collection_data = {
        "collection_id": "extent_test",
        "title": "Extent Test",
        "table_name": "extent_table",
    }
    create_response = await client.post(
        f"/projects/{project_id}/collections/",
        json=collection_data,
    )

    assert create_response.status_code == 201
    collection = create_response.json()

    assert "extent" in collection
    assert collection["extent"] is None
