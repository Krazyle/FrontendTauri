import json
from fastapi import APIRouter, Request, status

from app.collections.dependencies import CollectionServiceDependency
from app.collections.schemas import (
    CollectionCreate,
    CollectionRead,
    CollectionReplace,
    CollectionUpdate,
)
from app.proxy.service import proxy_request, rewrite_links
from config import get_settings

router = APIRouter(prefix="/projects/{project_id}/collections", tags=["collections"])
settings = get_settings()


@router.get("/", status_code=status.HTTP_200_OK)
async def list_collections(project_id: int, request: Request, service: CollectionServiceDependency):
    native_collections = await service.list_by_project(project_id)
    if not native_collections:
        return {"collections": [], "links": []}

    proxy_res = await proxy_request(request, "collections", settings)
    if proxy_res.status_code != 200:
        return proxy_res

    data = json.loads(bytes(proxy_res.body))

    mapping = {f"{c.schema_name}.{c.table_name}": c for c in native_collections}
    table_to_id = {f"{c.schema_name}.{c.table_name}": c.id for c in native_collections}

    enriched_collections = []
    for coll in data.get("collections", []):
        full_id = coll.get("id")
        if full_id in mapping:
            native = mapping[full_id]
            coll["title"] = native.title
            coll["description"] = native.description or coll.get("description")
            enriched_collections.append(coll)

    data["collections"] = enriched_collections
    return rewrite_links(data, project_id, settings, table_to_id)


@router.get("/{id}", status_code=status.HTTP_200_OK)
async def read_collection(
    project_id: int, id: int, request: Request, service: CollectionServiceDependency
):
    native = await service.get(project_id, id)
    full_id = f"{native.schema_name}.{native.table_name}"
    table_to_id = {full_id: native.id}

    proxy_res = await proxy_request(request, f"collections/{full_id}", settings)
    if proxy_res.status_code != 200:
        return proxy_res

    coll = json.loads(bytes(proxy_res.body))
    coll["title"] = native.title
    coll["description"] = native.description or coll.get("description")
    coll["status"] = native.status

    return rewrite_links(coll, project_id, settings, table_to_id)


@router.post("/", response_model=CollectionRead, status_code=status.HTTP_201_CREATED)
async def create_collection(
    project_id: int, collection: CollectionCreate, service: CollectionServiceDependency
) -> CollectionRead:
    return CollectionRead.model_validate(await service.create(project_id, collection))


@router.put("/{id}", response_model=CollectionRead, status_code=status.HTTP_200_OK)
async def replace_collection(
    project_id: int,
    id: int,
    collection: CollectionReplace,
    service: CollectionServiceDependency,
) -> CollectionRead:
    return CollectionRead.model_validate(await service.replace(project_id, id, collection))


@router.patch("/{id}", response_model=CollectionRead, status_code=status.HTTP_200_OK)
async def update_collection(
    project_id: int,
    id: int,
    collection: CollectionUpdate,
    service: CollectionServiceDependency,
) -> CollectionRead:
    return CollectionRead.model_validate(await service.update(project_id, id, collection))


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_collection(project_id: int, id: int, service: CollectionServiceDependency) -> None:
    await service.delete(project_id, id)
