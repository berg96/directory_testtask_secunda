import pytest

from app.domain.entities import BuildingEntity
from app.infrastructure.db.repositories.building import BuildingRepository


@pytest.mark.asyncio
async def test_get_buildings_within_radius(create_building, async_session):
    await create_building("ул. Тестовая, д.1", 54.8776, 20.3145)
    await create_building("ул. Продовая, д.7", 54.6543, 20.9087)

    repo = BuildingRepository(session=async_session)
    result = await repo.get_buildings_in_radius(54.8770, 20.3140, 15)
    assert all(isinstance(building, BuildingEntity) for building in result)
    assert len(result) == 1
