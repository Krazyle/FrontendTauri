import httpx
from fastapi import APIRouter, Request, Response, status
from fastapi.responses import StreamingResponse

from config import get_settings

router = APIRouter(tags=["proxy"])
settings = get_settings()


async def proxy_request(request: Request, path: str):
    url = f"{settings.pg_featureserv_url}/{path}"
    
    # Forward query parameters
    if request.query_params:
        url += f"?{request.query_params}"

    # Forward headers (excluding host to prevent routing issues)
    headers = {k: v for k, v in request.headers.items() if k.lower() not in ("host",)}

    async with httpx.AsyncClient() as client:
        # We only proxy GET requests for now as per Read-Only pg_featureserv
        try:
            proxy_res = await client.get(url, headers=headers, timeout=10.0)
            return Response(
                content=proxy_res.content,
                status_code=proxy_res.status_code,
                headers=dict(proxy_res.headers)
            )
        except httpx.RequestError as exc:
            return Response(
                content=f"Proxy error: {str(exc)}",
                status_code=status.HTTP_502_BAD_GATEWAY
            )


@router.get("/collections")
async def proxy_collections(request: Request):
    return await proxy_request(request, "collections")


@router.get("/collections/{collection_id}")
async def proxy_collection_detail(request: Request, collection_id: str):
    return await proxy_request(request, f"collections/{collection_id}")


@router.get("/collections/{collection_id}/items")
async def proxy_collection_items(request: Request, collection_id: str):
    return await proxy_request(request, f"collections/{collection_id}/items")


@router.get("/collections/{collection_id}/items/{item_id}")
async def proxy_item_detail(request: Request, collection_id: str, item_id: str):
    return await proxy_request(request, f"collections/{collection_id}/items/{item_id}")


@router.get("/functions")
async def proxy_functions(request: Request):
    return await proxy_request(request, "functions")


@router.get("/functions/{function_id}")
async def proxy_function_detail(request: Request, function_id: str):
    return await proxy_request(request, f"functions/{function_id}")


@router.get("/functions/{function_id}/items")
async def proxy_function_items(request: Request, function_id: str):
    return await proxy_request(request, f"functions/{function_id}/items")
