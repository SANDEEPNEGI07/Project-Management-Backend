from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.core.security import get_current_user
from app.models.users import UserModel
from app.schemas.user_profiles import (
    UserProfileCreate,
    UserProfileUpdate,
    UserProfileResponse,
)
from app.services.user_profile_service import (
    create_user_profile,
    get_user_profile,
    get_user_profile_by_user_id,
    get_user_profiles,
    update_user_profile,
    delete_user_profile,
)

router = APIRouter(tags=["User Profiles"])


@router.get("/", response_model=list[UserProfileResponse])
async def list_user_profiles(
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Return all user profiles."""
    return await get_user_profiles(db)


@router.post("/", response_model=UserProfileResponse, status_code=201)
async def add_user_profile(
    data: UserProfileCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Create a profile for the authenticated user."""
    return await create_user_profile(data, current_user.id, db)


@router.get("/me", response_model=UserProfileResponse)
async def read_my_profile(
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Get the profile that belongs to the authenticated user."""
    return await get_user_profile_by_user_id(current_user.id, db)


@router.patch("/me", response_model=UserProfileResponse)
async def edit_my_profile(
    data: UserProfileUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Update the authenticated user's own profile."""
    profile = await get_user_profile_by_user_id(current_user.id, db)
    return await update_user_profile(profile.id, data, current_user.id, db)


@router.delete("/me", status_code=204)
async def remove_my_profile(
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Delete the authenticated user's own profile."""
    profile = await get_user_profile_by_user_id(current_user.id, db)
    await delete_user_profile(profile.id, current_user.id, db)


@router.get("/{profile_id}", response_model=UserProfileResponse)
async def read_user_profile(
    profile_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Fetch a user profile by profile ID."""
    return await get_user_profile(profile_id, db)


@router.patch("/{profile_id}", response_model=UserProfileResponse)
async def edit_user_profile(
    profile_id: int,
    data: UserProfileUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Update a user profile by ID when authorized."""
    return await update_user_profile(profile_id, data, current_user.id, db)


@router.delete("/{profile_id}", status_code=204)
async def remove_user_profile(
    profile_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Delete a user profile by ID when authorized."""
    await delete_user_profile(profile_id, current_user.id, db)
