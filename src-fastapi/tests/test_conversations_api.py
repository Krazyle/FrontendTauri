import pytest
from httpx import AsyncClient


pytestmark = pytest.mark.asyncio


async def test_create_conversation(client: AsyncClient) -> None:
    response = await client.post(
        "/v1/conversations/",
        json={"title": "My Chat", "metadata": {"key": "val"}},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "My Chat"
    assert data["id"].startswith("conv_")


async def test_list_conversations(client: AsyncClient) -> None:
    await client.post("/v1/conversations/", json={"title": "Chat A"})
    await client.post("/v1/conversations/", json={"title": "Chat B"})

    response = await client.get("/v1/conversations/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Chat B"


async def test_read_conversation(client: AsyncClient) -> None:
    create_resp = await client.post("/v1/conversations/", json={"title": "My Chat"})
    conv_id = create_resp.json()["id"]

    response = await client.get(f"/v1/conversations/{conv_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "My Chat"


async def test_update_conversation(client: AsyncClient) -> None:
    create_resp = await client.post("/v1/conversations/", json={"title": "Old Title"})
    conv_id = create_resp.json()["id"]

    patch_resp = await client.patch(
        f"/v1/conversations/{conv_id}",
        json={"title": "New Title"},
    )
    assert patch_resp.status_code == 200
    assert patch_resp.json()["title"] == "New Title"


async def test_delete_conversation(client: AsyncClient) -> None:
    create_resp = await client.post("/v1/conversations/", json={"title": "To Delete"})
    conv_id = create_resp.json()["id"]

    delete_resp = await client.delete(f"/v1/conversations/{conv_id}")
    assert delete_resp.status_code == 204

    get_resp = await client.get(f"/v1/conversations/{conv_id}")
    assert get_resp.status_code == 404


async def test_conversation_not_found(client: AsyncClient) -> None:
    response = await client.get("/v1/conversations/nonexistent")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"]["identifier"] == "nonexistent"