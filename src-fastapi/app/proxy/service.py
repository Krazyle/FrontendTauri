import httpx
from typing import Any, Mapping
from fastapi import Request, Response, status
from config import Settings, get_settings


async def proxy_request(
    request: Request, path: str, settings: Settings | None = None
) -> Response:
    settings = settings or get_settings()
    url = f"{settings.pg_featureserv_url}/{path}"
    if request.query_params:
        url += f"?{request.query_params}"
    headers = {k: v for k, v in request.headers.items() if k.lower() not in ("host",)}
    async with httpx.AsyncClient() as client:
        try:
            proxy_res = await client.get(
                url, headers=headers, timeout=settings.proxy_timeout_seconds
            )
            return Response(
                content=proxy_res.content,
                status_code=proxy_res.status_code,
                headers=dict(proxy_res.headers),
            )
        except httpx.RequestError as exc:
            return Response(
                content=f"Proxy error: {str(exc)}",
                status_code=status.HTTP_502_BAD_GATEWAY,
            )


def rewrite_links(
    data: Any,
    project_id: int,
    settings: Settings | None = None,
    table_to_id: Mapping[str, int | None] | None = None,
) -> Any:
    settings = settings or get_settings()
    if isinstance(data, dict):
        new_data = {}
        for k, v in data.items():
            if k == "href" and isinstance(v, str):
                new_data[k] = _rewrite_url(v, project_id, settings, table_to_id)
            else:
                new_data[k] = rewrite_links(v, project_id, settings, table_to_id)
        return new_data
    elif isinstance(data, list):
        return [rewrite_links(i, project_id, settings, table_to_id) for i in data]
    return data


def _rewrite_url(
    url: str,
    project_id: int,
    settings: Settings | None = None,
    table_to_id: Mapping[str, int | None] | None = None,
) -> str:
    settings = settings or get_settings()
    if not url.startswith(settings.pg_featureserv_url):
        return url

    path = url.replace(settings.pg_featureserv_url, "").lstrip("/")
    base_url = f"{settings.app_external_url}/projects/{project_id}"

    if path.startswith("collections"):
        parts = path.split("/")
        if len(parts) > 1:
            table_name = parts[1]
            native_id = table_to_id.get(table_name, table_name) if table_to_id else table_name
            suffix = "/".join(parts[2:])
            new_path = f"collections/{native_id}"
            if suffix:
                new_path += f"/{suffix}"
            return f"{base_url}/{new_path}"
        return f"{base_url}/collections"

    if path.startswith("functions"):
        return f"{base_url}/{path}"

    return f"{base_url}/{path}"
