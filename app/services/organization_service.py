from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from app.models.organizations import OrganizationModel
from app.schemas.organizations import OrganizationCreate, OrganizationUpdate


async def create_organization(data: OrganizationCreate, db: AsyncSession) -> OrganizationModel:
    organization = OrganizationModel(**data.model_dump())
    db.add(organization)
    await db.commit()
    await db.refresh(organization)
    return organization


async def get_organization(org_id: int, db: AsyncSession) -> OrganizationModel:
    result = await db.execute(select(OrganizationModel).where(OrganizationModel.id == org_id))
    org = result.scalar_one_or_none()
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org


async def get_organizations(db: AsyncSession) -> list[OrganizationModel]:
    result = await db.execute(select(OrganizationModel))
    return list(result.scalars().all())


async def update_organization(org_id: int, data: OrganizationUpdate, db: AsyncSession) -> OrganizationModel:
    org = await get_organization(org_id, db)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(org, field, value)
    await db.commit()
    await db.refresh(org)
    return org


async def delete_organization(org_id: int, db: AsyncSession) -> None:
    org = await get_organization(org_id, db)
    await db.delete(org)
    await db.commit()
