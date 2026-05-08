from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.projects import projects_router
from app.collections import collections_router
from app.items import items_router
from app.proxy import proxy_router
from app.responses import responses_router
from app.conversations import conversations_router
from config import get_settings

settings = get_settings()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(projects_router)
app.include_router(collections_router)
app.include_router(items_router)
app.include_router(proxy_router)
app.include_router(responses_router)
app.include_router(conversations_router)


@app.get("/")
async def root():
    return {"message": "OK"}


@app.get("/health")
async def health():
    return {"status": "healthy"}
