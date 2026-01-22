import pytest


@pytest.mark.asyncio
async def test_success_get_buildings_in_radius(async_client, auth_headers, create_building):
    building1 = await create_building("ул. Тестовая, д.1", 54.7104, 20.4522)
    building2 = await create_building("ул. Продовая, д.7", 54.7260, 20.4605)
    building3 = await create_building("ул. Стендовая, д.15", 55.7558, 37.6176)
    latitude = 54.7182
    longitude = 20.4563
    radius_km = 5
    response = await async_client.get(
        f"/api/buildings/geo/radius?latitude={latitude}&longitude={longitude}&radius_km={radius_km}",
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 2
    assert len(data["items"]) == data["count"] == 2
    building_ids = [building["id"] for building in data["items"]]
    assert building1.id in building_ids and building2.id in building_ids
    assert building3.id not in building_ids


@pytest.mark.asyncio
async def test_get_organization_by_id_not_auth(async_client, create_organization):
    latitude = 54.7182
    longitude = 20.4563
    radius_km = 5
    response = await async_client.get(
        f"/api/buildings/geo/radius?latitude={latitude}&longitude={longitude}&radius_km={radius_km}"
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_success_get_buildings_in_radius_empty_resp(async_client, auth_headers, create_building):
    await create_building("ул. Тестовая, д.1", 54.7104, 20.4522)
    await create_building("ул. Продовая, д.7", 54.7260, 20.4605)
    await create_building("ул. Стендовая, д.15", 55.7558, 37.6176)
    latitude = 50.7182
    longitude = 20.4563
    radius_km = 5
    response = await async_client.get(
        f"/api/buildings/geo/radius?latitude={latitude}&longitude={longitude}&radius_km={radius_km}",
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 0
    assert data["items"] == []
