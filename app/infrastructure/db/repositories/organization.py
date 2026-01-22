from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.domain.entities import OrganizationEntity
from app.infrastructure.db import Category, Organization


class OrganizationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, organization_id: int) -> Optional[OrganizationEntity]:
        query = (
            select(Organization)
            .where(Organization.id == organization_id)
            .options(
                selectinload(Organization.categories),
                selectinload(Organization.phones),
                selectinload(Organization.building),
            )
        )
        result = await self.session.execute(query)
        orm_obj = result.scalar_one_or_none()
        if orm_obj is None:
            return None
        return OrganizationEntity.from_orm(orm_obj)

    async def get_by_building_id(self, building_id: int) -> list[OrganizationEntity]:
        query = (
            select(Organization)
            .where(Organization.building_id == building_id)
            .options(
                selectinload(Organization.categories),
                selectinload(Organization.phones),
                selectinload(Organization.building),
            )
        )
        result = await self.session.execute(query)
        return [OrganizationEntity.from_orm(organization) for organization in result.scalars().all()]

    async def get_by_category_id(self, category_id: int) -> list[OrganizationEntity]:
        query = (
            select(Organization)
            .join(Organization.categories)
            .where(Category.id == category_id)
            .options(
                selectinload(Organization.categories),
                selectinload(Organization.phones),
                selectinload(Organization.building),
            )
        )
        result = await self.session.execute(query)
        return [OrganizationEntity.from_orm(organization) for organization in result.scalars().all()]

    async def search_by_name(self, query: str) -> list[OrganizationEntity]:
        stmt = (
            select(Organization)
            .where(Organization.name.ilike(f"%{query}%"))
            .options(
                selectinload(Organization.categories),
                selectinload(Organization.phones),
                selectinload(Organization.building),
            )
            .order_by(Organization.name)
        )
        result = await self.session.execute(stmt)
        return [OrganizationEntity.from_orm(organization) for organization in result.scalars().all()]
