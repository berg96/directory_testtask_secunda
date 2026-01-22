import pytest

from app.services.building import BuildingService


@pytest.mark.asyncio
async def test_get_buildings_within_radius(create_building, async_session):
    building1 = await create_building("ул. Тестовая, д.1", 54.8776, 20.3145)
    await create_building("ул. Продовая, д.7", 54.6543, 20.9087)

    service = BuildingService(async_session)
    result = await service.get_buildings_in_radius(54.8770, 20.3140, 15)
    assert len(result) == 1
    assert building1.id == result[0].id
