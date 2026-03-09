from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.core.security import get_current_user
from app.models.users import UserModel
from app.schemas.projects import ProjectCreate, ProjectUpdate, ProjectResponse
from app.services.project_service import (
    create_project,
    get_project,
    get_projects,
    update_project,
    delete_project,
)

router = APIRouter(tags=["Projects"])


@router.get("/", response_model=list[ProjectResponse])
async def list_projects(
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    return await get_projects(db)


@router.post("/", response_model=ProjectResponse, status_code=201)
async def add_project(
    data: ProjectCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    return await create_project(data, db)


@router.get("/{project_id}", response_model=ProjectResponse)
async def read_project(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    return await get_project(project_id, db)


@router.patch("/{project_id}", response_model=ProjectResponse)
async def edit_project(
    project_id: int,
    data: ProjectUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    return await update_project(project_id, data, db)


@router.delete("/{project_id}", status_code=204)
async def remove_project(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    await delete_project(project_id, db)
