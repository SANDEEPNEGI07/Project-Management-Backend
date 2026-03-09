from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from app.models.user_profiles import UserProfileModel
from app.schemas.user_profiles import UserProfileCreate, UserProfileUpdate


async def create_user_profile(data: UserProfileCreate, db: AsyncSession) -> UserProfileModel:
    profile = UserProfileModel(**data.model_dump())
    db.add(profile)
    await db.commit()
    await db.refresh(profile)
    return profile


async def get_user_profile(profile_id: int, db: AsyncSession) -> UserProfileModel:
    result = await db.execute(select(UserProfileModel).where(UserProfileModel.id == profile_id))
    profile = result.scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=404, detail="User profile not found")
    return profile


async def get_user_profile_by_user_id(user_id: int, db: AsyncSession) -> UserProfileModel:
    result = await db.execute(select(UserProfileModel).where(UserProfileModel.userId == user_id))
    profile = result.scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=404, detail="User profile not found")
    return profile


async def get_user_profiles(db: AsyncSession) -> list[UserProfileModel]:
    result = await db.execute(select(UserProfileModel))
    return list(result.scalars().all())


async def update_user_profile(profile_id: int, data: UserProfileUpdate, db: AsyncSession) -> UserProfileModel:
    profile = await get_user_profile(profile_id, db)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(profile, field, value)
    await db.commit()
    await db.refresh(profile)
    return profile


async def delete_user_profile(profile_id: int, db: AsyncSession) -> None:
    profile = await get_user_profile(profile_id, db)
    await db.delete(profile)
    await db.commit()
