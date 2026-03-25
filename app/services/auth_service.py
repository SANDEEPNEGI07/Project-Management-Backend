from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from app.models.users import UserModel
from app.core.security import hash_password, verify_password, create_access_token


async def register_user(email: str, password: str, db: AsyncSession) -> UserModel:
    """Register a user or return the existing user."""
    result = await db.execute(select(UserModel).where(UserModel.email == email))
    existing = result.scalar_one_or_none()
    if existing:
        if verify_password(password, existing.password):
            return existing
        raise HTTPException(status_code=409, detail="Email already registered")

    user = UserModel(email=email, password=hash_password(password))
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def authenticate_user(email: str, password: str, db: AsyncSession) -> UserModel:
    """Validate credentials and return the matching user."""
    result = await db.execute(select(UserModel).where(UserModel.email == email))
    user = result.scalar_one_or_none()
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return user


def generate_token_for_user(user: UserModel) -> str:
    """Generate a JWT access token for the given user."""
    return create_access_token(data={"sub": str(user.id)})
