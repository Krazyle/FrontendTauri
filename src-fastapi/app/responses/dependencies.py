from typing import Annotated

from fastapi import Depends
from database import DatabaseSessionDependency
from app.responses.service import ResponseService


def get_response_service(session: DatabaseSessionDependency) -> ResponseService:
    return ResponseService(session)


ResponseServiceDependency = Annotated[ResponseService, Depends(get_response_service)]