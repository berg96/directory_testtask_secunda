import pytest

from app.services.organization import OrganizationService


@pytest.mark.asyncio
async def test_get_by_id(async_session, create_organization):
    org = await create_organization("ООО Тест")
    service = OrganizationService(async_session)

    result = await service.get_by_id(org.id)
    assert result is not None
    assert result.name == "ООО Тест"


@pytest.mark.asyncio
async def test_get_by_building_id(async_session, create_building, create_organization):
    building = await create_building("ул. Тестовая, д.1", 54.8776, 20.3145)
    org1 = await create_organization("ООО Тест", building_id=building.id)
    org2 = await create_organization("ОАО Прод", building_id=building.id)

    service = OrganizationService(async_session)
    result = await service.get_by_building_id(building.id)

    assert len(result) == 2
    ids = [organization.id for organization in result]
    assert org1.id in ids
    assert org2.id in ids


@pytest.mark.asyncio
async def test_get_by_category_id(async_session, create_category, create_organization):
    eat = await create_category("Еда")
    milk = await create_category("Молочная продукция", base_category_id=eat.id)

    org1 = await create_organization("ООО Тест", category_ids=[eat.id])
    org2 = await create_organization("ОАО Прод", category_ids=[milk.id])

    service = OrganizationService(async_session)
    result = await service.get_by_category_id(eat.id)

    ids = [organization.id for organization in result]
    assert org1.id in ids
    assert org2.id not in ids


@pytest.mark.asyncio
async def test_search_by_name(async_session, create_organization):
    org1 = await create_organization("ООО Тест")
    org2 = await create_organization("ОАО Прод")
    org3 = await create_organization("ЗАО Продакшн")

    service = OrganizationService(async_session)
    result = await service.search_by_name("прод")

    ids = [organization.id for organization in result]
    assert org2.id in ids
    assert org3.id in ids
    assert org1.id not in ids


@pytest.mark.asyncio
async def test_get_organizations_in_radius(async_session, create_building, create_organization):
    building1 = await create_building("ул. Тестовая, д.1", 54.8776, 20.3145)
    building2 = await create_building("ул. Продовая, д.7", 54.8770, 20.3140)

    org1 = await create_organization("ООО Тест", building_id=building1.id)
    org2 = await create_organization("ОАО Прод", building_id=building2.id)
    org3 = await create_organization("ЗАО Продакшн")

    service = OrganizationService(async_session)
    result = await service.get_organizations_in_radius(54.8773, 20.3142, radius_km=15.0)

    ids = [organization.id for organization in result]
    assert org1.id in ids
    assert org2.id in ids
    assert org3.id not in ids


@pytest.mark.asyncio
async def test_get_by_nested_categories(async_session, create_category, create_organization):
    eat = await create_category("Еда")
    meat = await create_category("Мясная продукция", base_category_id=eat.id)
    milk = await create_category("Молочная продукция", base_category_id=eat.id)

    org1 = await create_organization("ООО Тест", category_ids=[eat.id])
    org2 = await create_organization("ОАО Прод", category_ids=[meat.id])
    org3 = await create_organization("ЗАО Продакшн", category_ids=[milk.id])

    service = OrganizationService(async_session)
    result = await service.get_by_nested_categories(eat.id)

    ids = [organization.id for organization in result]
    assert org1.id in ids
    assert org2.id in ids
    assert org3.id in ids
