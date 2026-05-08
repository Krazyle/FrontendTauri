import json

from fastapi import APIRouter, Request, Response

from app.proxy.service import proxy_request, rewrite_links
from config import get_settings

router = APIRouter(prefix="/projects/{project_id}", tags=["proxy"])
settings = get_settings()


@router.get("/functions")
async def proxy_functions(request: Request, project_id: int) -> Response:
    proxy_res = await proxy_request(request, "functions", settings)
    if proxy_res.status_code != 200:
        return proxy_res
    data = json.loads(bytes(proxy_res.body))
    return rewrite_links(data, project_id, settings)


@router.get("/functions/{function_id}")
async def proxy_function_detail(request: Request, project_id: int, function_id: str) -> Response:
    proxy_res = await proxy_request(request, f"functions/{function_id}", settings)
    if proxy_res.status_code != 200:
        return proxy_res
    data = json.loads(bytes(proxy_res.body))
    return rewrite_links(data, project_id, settings)


@router.get("/functions/{function_id}/items")
async def proxy_function_items(request: Request, project_id: int, function_id: str) -> Response:
    proxy_res = await proxy_request(request, f"functions/{function_id}/items", settings)
    if proxy_res.status_code != 200:
        return proxy_res
    data = json.loads(bytes(proxy_res.body))
    return rewrite_links(data, project_id, settings)
