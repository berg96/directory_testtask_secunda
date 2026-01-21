from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities import BuildingEntity
from app.infrastructure.db.repositories.building import BuildingRepository


class BuildingService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = BuildingRepository(session)

    async def get_buildings_in_radius(
        self, latitude: float, longitude: float, radius_km: float
    ) -> list[BuildingEntity]:
        return await self.repo.get_buildings_in_radius(latitude, longitude, radius_km)
