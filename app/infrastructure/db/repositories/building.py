from geoalchemy2.functions import ST_Distance, ST_DWithin
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities import BuildingEntity
from app.infrastructure.db import Building


class BuildingRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def exists(self, building_id: int) -> bool:
        query = select(Building.id).where(Building.id == building_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none() is not None

    async def get_buildings_in_radius(
        self, latitude: float, longitude: float, radius_km: float
    ) -> list[BuildingEntity]:
        point = func.ST_SetSRID(func.ST_MakePoint(longitude, latitude), 4326)

        query = (
            select(Building)
            .where(ST_DWithin(Building.location, point, radius_km * 1000))
            .order_by(ST_Distance(Building.location, point))
        )

        result = await self.session.execute(query)
        return [BuildingEntity.from_orm(building) for building in result.scalars().all()]
