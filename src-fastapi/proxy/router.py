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

    async with httpx.AsyncClient() as client:
        # We only proxy GET requests for now as per Read-Only pg_featureserv
        try:
            proxy_res = await client.get(url, timeout=10.0)
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
