from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.core.config import settings
from app.models.users import UserModel
from app.schemas.users import UserCreate, UserResponse
from app.services.auth_service import (
    register_user,
    authenticate_user,
    generate_token_for_user,
)

router = APIRouter(tags=["Auth"])


@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate, response: Response, db: AsyncSession = Depends(get_db)):
    existing = await db.execute(
        select(UserModel).where(UserModel.email == user_data.email)
    )
    already_exists = existing.scalar_one_or_none() is not None

    user = await register_user(user_data.email, user_data.password, db)

    response.status_code = 200 if already_exists else 201
    return user


@router.post("/login")
async def login(
    user_data: UserCreate,
    response: Response,
    db: AsyncSession = Depends(get_db),
):
    user = await authenticate_user(user_data.email, user_data.password, db)
    token = generate_token_for_user(user)
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite="lax",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
    return {"message": "Login successful"}


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"message": "Logged out"}
