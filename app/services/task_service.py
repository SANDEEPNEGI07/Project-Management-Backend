from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from app.models.tasks import TaskModel
from app.schemas.tasks import TaskCreate, TaskUpdate


async def create_task(data: TaskCreate, db: AsyncSession) -> TaskModel:
    """Create and persist a new task."""
    task = TaskModel(**data.model_dump())
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task


async def get_task(task_id: int, db: AsyncSession) -> TaskModel:
    """Return one task by ID or raise 404 if missing."""
    result = await db.execute(select(TaskModel).where(TaskModel.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


async def get_tasks(db: AsyncSession) -> list[TaskModel]:
    """Return all tasks."""
    result = await db.execute(select(TaskModel))
    return list(result.scalars().all())


async def update_task(task_id: int, data: TaskUpdate, db: AsyncSession) -> TaskModel:
    """Apply partial updates to a task and persist changes."""
    task = await get_task(task_id, db)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(task, field, value)
    await db.commit()
    await db.refresh(task)
    return task


async def delete_task(task_id: int, db: AsyncSession) -> None:
    """Delete a task by ID."""
    task = await get_task(task_id, db)
    await db.delete(task)
    await db.commit()
