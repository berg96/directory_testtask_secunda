import pytest


@pytest.mark.asyncio
async def test_success_get_organization_by_id(
    async_client, create_building, create_category, create_organization, create_phone, auth_headers
):
    building = await create_building("ул. Тестовая, д.1", 54.8776, 20.3145)
    eat = await create_category("Еда")
    organization = await create_organization("ООО Тест", building_id=building.id, category_ids=[eat.id])
    phone = await create_phone("+7 (999) 123-45-67", organization.id)

    response = await async_client.get(f"/api/organizations/{organization.id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == organization.id
    assert len(data["categories"]) == 1
    assert data["categories"][0]["id"] == eat.id
    assert data["building"]["id"] == building.id
    assert len(data["phones"]) == 1
    assert data["phones"][0]["id"] == phone.id


@pytest.mark.asyncio
async def test_get_organization_by_id_not_found(async_client, auth_headers):
    not_found_organization_id = 999
    response = await async_client.get(f"/api/organizations/{not_found_organization_id}", headers=auth_headers)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_organization_by_id_not_auth(async_client, create_organization):
    organization = await create_organization("ООО Тест")
    response = await async_client.get(f"/api/organizations/{organization.id}")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_organizations_by_building(async_client, create_building, create_organization, auth_headers):
    building1 = await create_building("ул. Тестовая, д.1", 54.8776, 20.3145)
    organization1 = await create_organization("ООО Тест", building_id=building1.id)
    building2 = await create_building("ул. Продовая, д.7", 54.3145, 20.8776)
    await create_organization("ОАО Прод", building_id=building2.id)
    response = await async_client.get(f"/api/organizations/building/{building1.id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 1
    assert len(data["items"]) == data["count"] == 1
    assert data["items"][0]["id"] == organization1.id


@pytest.mark.asyncio
async def test_get_organization_by_building_not_found(async_client, auth_headers):
    not_found_building_id = 999
    response = await async_client.get(f"/api/organizations/building/{not_found_building_id}", headers=auth_headers)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_by_category(async_client, auth_headers, create_category, create_organization):
    eat = await create_category("Еда")
    organization1 = await create_organization("ООО Тест", category_ids=[eat.id])
    furniture = await create_category("Мебель")
    await create_organization("ОАО Прод", category_ids=[furniture.id])
    response = await async_client.get(f"/api/organizations/category/{eat.id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 1
    assert len(data["items"]) == data["count"] == 1
    assert data["items"][0]["id"] == organization1.id


@pytest.mark.asyncio
async def test_get_organization_by_category_not_found(async_client, auth_headers):
    not_found_category_id = 999
    response = await async_client.get(f"/api/organizations/category/{not_found_category_id}", headers=auth_headers)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_by_nested_categories(async_client, auth_headers, create_category, create_organization):
    eat = await create_category("Еда")
    organization1 = await create_organization("ООО Тест", category_ids=[eat.id])
    milk = await create_category("Молочная продукция", base_category_id=eat.id)
    organization2 = await create_organization("ОАО Прод", category_ids=[milk.id])
    cheese = await create_category("Сыры", base_category_id=milk.id)
    organization3 = await create_organization("ЗАО Собес", category_ids=[cheese.id])
    response = await async_client.get(f"/api/organizations/nested-categories/{eat.id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 3
    assert len(data["items"]) == data["count"] == 3
    org_ids = [organization["id"] for organization in data["items"]]
    assert organization1.id in org_ids and organization2.id in org_ids and organization3.id in org_ids


@pytest.mark.asyncio
async def test_get_organization_by_nested_categories_not_found(async_client, auth_headers):
    not_found_category_id = 999
    response = await async_client.get(
        f"/api/organizations/nested-categories/{not_found_category_id}", headers=auth_headers
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_organizations_in_radius(async_client, auth_headers, create_building, create_organization):
    building1 = await create_building("ул. Тестовая, д.1", 54.7104, 20.4522)
    organization1 = await create_organization("ООО Тест", building_id=building1.id)
    building2 = await create_building("ул. Продовая, д.7", 54.7260, 20.4605)
    organization2 = await create_organization("ОАО Прод", building_id=building2.id)
    building3 = await create_building("ул. Стендовая, д.15", 55.7558, 37.6176)
    organization3 = await create_organization("ЗАО Собес", building_id=building3.id)
    latitude = 54.7182
    longitude = 20.4563
    radius_km = 5
    response = await async_client.get(
        f"/api/organizations/geo/radius?latitude={latitude}&longitude={longitude}&radius_km={radius_km}",
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 2
    assert len(data["items"]) == data["count"] == 2
    org_ids = [organization["id"] for organization in data["items"]]
    assert organization1.id in org_ids and organization2.id in org_ids
    assert organization3.id not in org_ids


@pytest.mark.asyncio
async def test_get_organizations_in_radius_empty_resp(async_client, auth_headers, create_building, create_organization):
    building1 = await create_building("ул. Тестовая, д.1", 54.7104, 20.4522)
    await create_organization("ООО Тест", building_id=building1.id)
    building2 = await create_building("ул. Продовая, д.7", 54.7260, 20.4605)
    await create_organization("ОАО Прод", building_id=building2.id)
    building3 = await create_building("ул. Стендовая, д.15", 55.7558, 37.6176)
    await create_organization("ЗАО Собес", building_id=building3.id)
    latitude = 50.7182
    longitude = 20.4563
    radius_km = 5
    response = await async_client.get(
        f"/api/organizations/geo/radius?latitude={latitude}&longitude={longitude}&radius_km={radius_km}",
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 0
    assert data["items"] == []


@pytest.mark.asyncio
async def test_search_organizations_by_name(async_client, auth_headers, create_organization):
    organization1 = await create_organization("ООО Тест")
    organization2 = await create_organization("ОАО Прод")
    organization3 = await create_organization("ЗАО Тестовый стенд")
    query = "тест"
    response = await async_client.get(f"/api/organizations/search?name={query}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 2
    assert len(data["items"]) == data["count"] == 2
    org_ids = [organization["id"] for organization in data["items"]]
    assert organization1.id in org_ids and organization3.id in org_ids
    assert organization2.id not in org_ids


@pytest.mark.asyncio
async def test_search_organizations_by_name_empty_resp(async_client, auth_headers, create_organization):
    await create_organization("ООО Тест")
    await create_organization("ОАО Прод")
    await create_organization("ЗАО Тестовый стенд")
    query = "собес"
    response = await async_client.get(f"/api/organizations/search?name={query}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 0
    assert data["items"] == []
