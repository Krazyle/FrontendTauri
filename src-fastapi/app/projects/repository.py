from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import col

from app.projects.models import Project
from app.projects.schemas import ProjectCreate, ProjectReplace, ProjectUpdate


class ProjectRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, project: ProjectCreate) -> Project:
        created_project = Project(
            name=project.name,
            description=project.description,
        )
        self.session.add(created_project)
        await self.session.commit()
        await self.session.refresh(created_project)
        return created_project

    async def list_all(self) -> list[Project]:
        statement = select(Project).order_by(col(Project.created_at), col(Project.id))
        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def get(self, project_id: int) -> Project | None:
        return await self.session.get(Project, project_id)

    async def replace(
        self,
        project_id: int,
        project: ProjectReplace,
    ) -> Project | None:
        existing_project = await self.get(project_id)
        if existing_project is None:
            return None

        existing_project.name = project.name
        existing_project.description = project.description
        await self.session.commit()
        await self.session.refresh(existing_project)
        return existing_project

    async def update(self, project_id: int, project: ProjectUpdate) -> Project | None:
        existing_project = await self.get(project_id)
        if existing_project is None:
            return None

        update_data = project.model_dump(exclude_unset=True)
        if not update_data:
            return existing_project

        for key, value in update_data.items():
            setattr(existing_project, key, value)

        await self.session.commit()
        await self.session.refresh(existing_project)
        return existing_project

    async def delete(self, project_id: int) -> bool:
        existing_project = await self.get(project_id)
        if existing_project is None:
            return False

        await self.session.delete(existing_project)
        await self.session.commit()
        return True
