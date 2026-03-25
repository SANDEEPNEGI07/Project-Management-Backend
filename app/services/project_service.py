from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from app.models.projects import ProjectModel
from app.schemas.projects import ProjectCreate, ProjectUpdate


async def create_project(data: ProjectCreate, db: AsyncSession) -> ProjectModel:
    """Create and persist a new project."""
    project = ProjectModel(**data.model_dump())
    db.add(project)
    await db.commit()
    await db.refresh(project)
    return project


async def get_project(project_id: int, db: AsyncSession) -> ProjectModel:
    """Return one project by ID or raise 404 if missing."""
    result = await db.execute(select(ProjectModel).where(ProjectModel.id == project_id))
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


async def get_projects(db: AsyncSession) -> list[ProjectModel]:
    """Return all projects."""
    result = await db.execute(select(ProjectModel))
    return list(result.scalars().all())


async def update_project(
    project_id: int, data: ProjectUpdate, db: AsyncSession,
) -> ProjectModel:
    """Apply partial updates to a project and persist changes."""
    project = await get_project(project_id, db)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(project, field, value)
    await db.commit()
    await db.refresh(project)
    return project


async def delete_project(project_id: int, db: AsyncSession) -> None:
    """Delete a project by ID."""
    project = await get_project(project_id, db)
    await db.delete(project)
    await db.commit()
