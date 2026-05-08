from fastapi import FastAPI

from projects import projects_router

app = FastAPI()

app.include_router(projects_router)


@app.get("/")
async def root():
    return {"message": "OK"}


@app.get("/health")
async def health():
    return {"status": "healthy"}
