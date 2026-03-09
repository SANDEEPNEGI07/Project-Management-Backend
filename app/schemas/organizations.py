from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.core.enums import OrganizationStatus


class OrganizationBase(BaseModel):
    name: str
    description: Optional[str] = None
    status: OrganizationStatus = OrganizationStatus.ACTIVE


class OrganizationCreate(OrganizationBase):
    pass


class OrganizationUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[OrganizationStatus] = None


class OrganizationResponse(OrganizationBase):
    id: int
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True
