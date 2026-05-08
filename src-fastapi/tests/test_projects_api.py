import pytest
from httpx import AsyncClient


pytestmark = pytest.mark.asyncio


async def test_create_read_list_replace_patch_and_delete_project(
    client: AsyncClient,
) -> None:
    create_response = await client.post(
        "/projects/",
        json={"name": "  Alpha  ", "description": "Initial"},
    )

    assert create_response.status_code == 201
    created_project = create_response.json()
    assert created_project["name"] == "Alpha"
    assert created_project["description"] == "Initial"

    list_response = await client.get("/projects/")
    assert list_response.status_code == 200
    listed_projects = list_response.json()
    assert [project["id"] for project in listed_projects] == [created_project["id"]]

    read_response = await client.get(f"/projects/{created_project['id']}")
    assert read_response.status_code == 200
    assert read_response.json()["id"] == created_project["id"]

    replace_response = await client.put(
        f"/projects/{created_project['id']}",
        json={"name": "Beta"},
    )
    assert replace_response.status_code == 200
    assert replace_response.json()["name"] == "Beta"
    assert replace_response.json()["description"] is None
    assert replace_response.json()["updated_at"] != created_project["updated_at"]

    patch_response = await client.patch(
        f"/projects/{created_project['id']}",
        json={"description": "Patched"},
    )
    assert patch_response.status_code == 200
    assert patch_response.json()["name"] == "Beta"
    assert patch_response.json()["description"] == "Patched"

    delete_response = await client.delete(f"/projects/{created_project['id']}")
    assert delete_response.status_code == 204
    assert delete_response.content == b""

    missing_response = await client.get(f"/projects/{created_project['id']}")
    assert missing_response.status_code == 404
    assert missing_response.json() == {"detail": "Project not found"}


async def test_duplicate_project_names_are_allowed(client: AsyncClient) -> None:
    first_response = await client.post("/projects/", json={"name": "Map"})
    duplicate_response = await client.post("/projects/", json={"name": "map"})

    assert first_response.status_code == 201
    assert duplicate_response.status_code == 201

    list_response = await client.get("/projects/")
    assert [project["name"] for project in list_response.json()] == ["Map", "map"]


async def test_duplicate_project_name_patch_is_allowed(
    client: AsyncClient,
) -> None:
    first_response = await client.post("/projects/", json={"name": "Map"})
    second_response = await client.post("/projects/", json={"name": "Survey"})

    assert first_response.status_code == 201
    assert second_response.status_code == 201

    duplicate_response = await client.patch(
        f"/projects/{second_response.json()['id']}",
        json={"name": "map"},
    )

    assert duplicate_response.status_code == 200
    assert duplicate_response.json()["name"] == "map"


async def test_patch_distinguishes_omitted_description_from_null(
    client: AsyncClient,
) -> None:
    create_response = await client.post(
        "/projects/",
        json={"name": "Patch target", "description": "Keep me"},
    )
    project_id = create_response.json()["id"]

    omitted_response = await client.patch(
        f"/projects/{project_id}",
        json={"name": "Renamed"},
    )
    assert omitted_response.status_code == 200
    assert omitted_response.json()["name"] == "Renamed"
    assert omitted_response.json()["description"] == "Keep me"

    null_response = await client.patch(
        f"/projects/{project_id}",
        json={"description": None},
    )
    assert null_response.status_code == 200
    assert null_response.json()["description"] is None


async def test_empty_patch_is_noop(client: AsyncClient) -> None:
    create_response = await client.post("/projects/", json={"name": "Noop target"})
    created_project = create_response.json()

    patch_response = await client.patch(f"/projects/{created_project['id']}", json={})

    assert patch_response.status_code == 200
    assert patch_response.json()["updated_at"] == created_project["updated_at"]


async def test_list_projects_returns_all_projects(client: AsyncClient) -> None:
    for name in ("Alpha", "Bravo", "Charlie"):
        response = await client.post("/projects/", json={"name": name})
        assert response.status_code == 201

    response = await client.get("/projects/")

    assert response.status_code == 200
    assert [project["name"] for project in response.json()] == [
        "Alpha",
        "Bravo",
        "Charlie",
    ]


async def test_missing_project_returns_404(client: AsyncClient) -> None:
    response = await client.get("/projects/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Project not found"}
