from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserProfileBase(BaseModel):
    username: str
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    bio: Optional[str] = None
    phone: Optional[str] = None
    avatarUrl: Optional[str] = None


class UserProfileCreate(UserProfileBase):
    pass


class UserProfileUpdate(BaseModel):
    username: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    bio: Optional[str] = None
    phone: Optional[str] = None
    avatarUrl: Optional[str] = None


class UserProfileResponse(UserProfileBase):
    id: int
    userId: int
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True
