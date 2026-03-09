from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.core.security import get_current_user
from app.models.users import UserModel
from app.schemas.users import UserResponse, UserUpdate
from app.services.user_service import get_users, get_user, update_user, delete_user

router = APIRouter(tags=["Users"])


@router.get("/me", response_model=UserResponse)
async def read_me(current_user: UserModel = Depends(get_current_user)):
    return current_user


@router.get("/", response_model=list[UserResponse])
async def list_users(
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    return await get_users(db)


@router.get("/{user_id}", response_model=UserResponse)
async def read_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    return await get_user(user_id, db)


@router.patch("/{user_id}", response_model=UserResponse)
async def edit_user(
    user_id: int,
    data: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    return await update_user(user_id, data, db)


@router.delete("/{user_id}", status_code=204)
async def remove_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    await delete_user(user_id, db)
