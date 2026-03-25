from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from app.models.users import UserModel
from app.schemas.users import UserUpdate
from app.core.security import hash_password


async def get_user(user_id: int, db: AsyncSession) -> UserModel:
    """Return one user by ID or raise 404 if missing."""
    result = await db.execute(select(UserModel).where(UserModel.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def get_users(db: AsyncSession) -> list[UserModel]:
    """Return all users."""
    result = await db.execute(select(UserModel))
    return list(result.scalars().all())


async def update_user(user_id: int, data: UserUpdate, db: AsyncSession) -> UserModel:
    """Apply partial updates to a user and hash password when provided."""
    user = await get_user(user_id, db)
    update_data = data.model_dump(exclude_unset=True)
    if "password" in update_data:
        update_data["password"] = hash_password(update_data["password"])
    for field, value in update_data.items():
        setattr(user, field, value)
    await db.commit()
    await db.refresh(user)
    return user


async def delete_user(user_id: int, db: AsyncSession) -> None:
    """Delete a user by ID."""
    user = await get_user(user_id, db)
    await db.delete(user)
    await db.commit()
