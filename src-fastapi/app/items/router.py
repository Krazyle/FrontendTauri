import json
from fastapi import APIRouter, Request, status
from app.items.dependencies import ItemServiceDependency
from app.items.schemas import ItemCreate, ItemRead, ItemUpdate
from app.proxy.service import proxy_request, rewrite_links
from config import get_settings

router = APIRouter(
    prefix="/projects/{project_id}/collections/{collection_id}/items", tags=["items"]
)
settings = get_settings()


@router.get("/", status_code=status.HTTP_200_OK)
async def list_items(
    project_id: int,
    collection_id: int,
    request: Request,
    service: ItemServiceDependency,
):
    collection = await service.collection_service.get(project_id, collection_id)
    full_table_name = f"{collection.schema_name}.{collection.table_name}"
    table_to_id = {full_table_name: collection_id}

    proxy_res = await proxy_request(request, f"collections/{full_table_name}/items", settings)
    if proxy_res.status_code != 200:
        return proxy_res

    data = json.loads(bytes(proxy_res.body))
    return rewrite_links(data, project_id, settings, table_to_id)


@router.post("/", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
async def create_item(
    project_id: int,
    collection_id: int,
    item: ItemCreate,
    service: ItemServiceDependency,
) -> ItemRead:
    return ItemRead.model_validate(await service.create(project_id, collection_id, item))


@router.get("/{feature_id}", status_code=status.HTTP_200_OK)
async def read_item(
    project_id: int,
    collection_id: int,
    feature_id: str,
    request: Request,
    service: ItemServiceDependency,
):
    collection = await service.collection_service.get(project_id, collection_id)
    full_table_name = f"{collection.schema_name}.{collection.table_name}"
    table_to_id = {full_table_name: collection_id}

    proxy_res = await proxy_request(
        request, f"collections/{full_table_name}/items/{feature_id}", settings
    )
    if proxy_res.status_code != 200:
        return proxy_res

    data = json.loads(bytes(proxy_res.body))
    return rewrite_links(data, project_id, settings, table_to_id)


@router.patch("/{feature_id}", response_model=ItemRead, status_code=status.HTTP_200_OK)
async def update_item(
    project_id: int,
    collection_id: int,
    feature_id: str,
    item: ItemUpdate,
    service: ItemServiceDependency,
) -> ItemRead:
    return ItemRead.model_validate(
        await service.update(project_id, collection_id, feature_id, item)
    )


@router.delete("/{feature_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
    project_id: int, collection_id: int, feature_id: str, service: ItemServiceDependency
) -> None:
    await service.delete(project_id, collection_id, feature_id)
