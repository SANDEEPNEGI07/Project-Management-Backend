from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.core.config import settings
from app.schemas.users import UserCreate, UserResponse
from app.services.auth_service import register_user, authenticate_user, generate_token_for_user

router = APIRouter(tags=["Auth"])


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    user = await register_user(user_data.email, user_data.password, db)
    return user


@router.post("/login")
async def login(user_data: UserCreate, response: Response, db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(user_data.email, user_data.password, db)
    token = generate_token_for_user(user)
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
    return {"message": "Login successful"}


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"message": "Logged out"}
