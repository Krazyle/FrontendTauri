from fastapi import FastAPI

from projects import projects_router
from collections import collections_router
from items import items_router
from proxy import proxy_router

app = FastAPI()

app.include_router(projects_router)
app.include_router(collections_router)
app.include_router(items_router)
app.include_router(proxy_router)


@app.get("/")
async def root():
    return {"message": "OK"}


@app.get("/health")
async def health():
    return {"status": "healthy"}
