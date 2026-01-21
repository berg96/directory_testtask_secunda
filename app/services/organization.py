import asyncio
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities import OrganizationEntity
from app.domain.exceptions import BuildingNotFoundError, CategoryNotFoundError
from app.infrastructure.db.repositories.building import BuildingRepository
from app.infrastructure.db.repositories.category import CategoryRepository
from app.infrastructure.db.repositories.organization import OrganizationRepository


class OrganizationService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = OrganizationRepository(session)
        self.building_repo = BuildingRepository(session)
        self.category_repo = CategoryRepository(session)

    async def get_by_id(self, organization_id: int) -> Optional[OrganizationEntity]:
        return await self.repo.get_by_id(organization_id)

    async def get_by_building_id(self, building_id: int) -> list[OrganizationEntity]:
        if not await self.building_repo.exists(building_id):
            raise BuildingNotFoundError(identifier=building_id)
        return await self.repo.get_by_building_id(building_id)

    async def get_by_category_id(self, category_id: int) -> list[OrganizationEntity]:
        if not await self.category_repo.exists(category_id):
            raise CategoryNotFoundError(identifier=category_id)
        return await self.repo.get_by_category_id(category_id)

    async def search_by_name(self, query: str) -> list[OrganizationEntity]:
        return await self.repo.search_by_name(query)

    async def get_organizations_in_radius(
        self, latitude: float, longitude: float, radius_km: float
    ) -> list[OrganizationEntity]:
        buildings = await self.building_repo.get_buildings_in_radius(latitude, longitude, radius_km)
        tasks = [self.repo.get_by_building_id(building.id) for building in buildings]
        results = await asyncio.gather(*tasks)
        return [organization for sublist in results for organization in sublist]

    async def get_by_nested_categories(self, category_id: int) -> list[OrganizationEntity]:
        if not await self.category_repo.exists(category_id):
            raise CategoryNotFoundError(identifier=category_id)
        categories = await self.category_repo.get_category_with_nested_categories(category_id)
        tasks = [self.repo.get_by_category_id(category.id) for category in categories]
        results = await asyncio.gather(*tasks)
        return list(set(organization for sublist in results for organization in sublist))
