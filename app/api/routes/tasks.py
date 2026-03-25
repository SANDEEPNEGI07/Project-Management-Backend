from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.core.security import get_current_user
from app.models.users import UserModel
from app.schemas.tasks import TaskCreate, TaskUpdate, TaskResponse
from app.services.task_service import (
    create_task,
    get_task,
    get_tasks,
    update_task,
    delete_task,
)

router = APIRouter(tags=["Tasks"])


@router.get("/", response_model=list[TaskResponse])
async def list_tasks(
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Return all tasks."""
    return await get_tasks(db)


@router.post("/", response_model=TaskResponse, status_code=201)
async def add_task(
    data: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Create a new task."""
    return await create_task(data, db)


@router.get("/{task_id}", response_model=TaskResponse)
async def read_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Fetch a task by ID."""
    return await get_task(task_id, db)


@router.patch("/{task_id}", response_model=TaskResponse)
async def edit_task(
    task_id: int,
    data: TaskUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Update a task by ID."""
    return await update_task(task_id, data, db)


@router.delete("/{task_id}", status_code=204)
async def remove_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Delete a task by ID."""
    await delete_task(task_id, db)
