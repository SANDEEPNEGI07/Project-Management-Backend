from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from app.models.user_profiles import UserProfileModel
from app.schemas.user_profiles import UserProfileCreate, UserProfileUpdate


async def create_user_profile(
    data: UserProfileCreate, user_id: int, db: AsyncSession,
) -> UserProfileModel:
    """Create a profile for a user if one does not already exist."""
    existing = await db.execute(
        select(UserProfileModel)
        .where(UserProfileModel.userId == user_id)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=409,
            detail="A profile already exists for this user",
        )
    profile = UserProfileModel(**data.model_dump(), userId=user_id)
    db.add(profile)
    await db.commit()
    await db.refresh(profile)
    return profile


async def get_user_profile(
    profile_id: int, db: AsyncSession,
) -> UserProfileModel:
    """Return one user profile by ID or raise 404 if missing."""
    result = await db.execute(
        select(UserProfileModel)
        .where(UserProfileModel.id == profile_id)
    )
    profile = result.scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=404, detail="User profile not found")
    return profile


async def get_user_profile_by_user_id(
    user_id: int, db: AsyncSession,
) -> UserProfileModel:
    """Return a user profile by owning user ID or raise 404 if missing."""
    result = await db.execute(
        select(UserProfileModel)
        .where(UserProfileModel.userId == user_id)
    )
    profile = result.scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=404, detail="User profile not found")
    return profile


async def get_user_profiles(db: AsyncSession) -> list[UserProfileModel]:
    """Return all user profiles."""
    result = await db.execute(select(UserProfileModel))
    return list(result.scalars().all())


async def update_user_profile(
    profile_id: int, data: UserProfileUpdate,
    user_id: int, db: AsyncSession,
) -> UserProfileModel:
    """Update a user profile when the caller owns that profile."""
    profile = await get_user_profile(profile_id, db)
    if profile.userId != user_id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to update this profile"
        )
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(profile, field, value)
    await db.commit()
    await db.refresh(profile)
    return profile


async def delete_user_profile(
    profile_id: int, user_id: int, db: AsyncSession,
) -> None:
    """Delete a user profile when the caller owns that profile."""
    profile = await get_user_profile(profile_id, db)
    if profile.userId != user_id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to delete this profile"
        )
    await db.delete(profile)
    await db.commit()
