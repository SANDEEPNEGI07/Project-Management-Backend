from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.core.security import get_current_user
from app.models.users import UserModel
from app.schemas.organizations import OrganizationCreate, OrganizationUpdate, OrganizationResponse
from app.services.organization_service import (
    create_organization,
    get_organization,
    get_organizations,
    update_organization,
    delete_organization,
)

router = APIRouter(tags=["Organizations"])


@router.get("/", response_model=list[OrganizationResponse])
async def list_organizations(db: AsyncSession = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    return await get_organizations(db)


@router.post("/", response_model=OrganizationResponse, status_code=201)
async def add_organization(data: OrganizationCreate, db: AsyncSession = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    return await create_organization(data, db)


@router.get("/{org_id}", response_model=OrganizationResponse)
async def read_organization(org_id: int, db: AsyncSession = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    return await get_organization(org_id, db)


@router.patch("/{org_id}", response_model=OrganizationResponse)
async def edit_organization(org_id: int, data: OrganizationUpdate, db: AsyncSession = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    return await update_organization(org_id, data, db)


@router.delete("/{org_id}", status_code=204)
async def remove_organization(org_id: int, db: AsyncSession = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    await delete_organization(org_id, db)
