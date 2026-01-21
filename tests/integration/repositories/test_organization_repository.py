import pytest

from app.infrastructure.db.repositories.organization import OrganizationRepository


@pytest.mark.asyncio
async def test_get_by_id(async_session, create_building, create_category, create_organization, create_phone):
    building = await create_building("ул. Тестовая, д.1", 54.8776, 20.3145)
    eat = await create_category("Еда")
    milk = await create_category("Молочная продукция", base_category_id=eat.id)
    cheese = await create_category("Сыры", base_category_id=milk.id)
    organization = await create_organization("ООО Тест", building.id, [eat.id, milk.id, cheese.id])
    phone = await create_phone("+7 (999) 123-45-67", organization.id)

    repo = OrganizationRepository(async_session)
    fetched = await repo.get_by_id(organization.id)

    assert fetched is not None
    assert fetched.name == "ООО Тест"
    assert fetched.building.id == building.id
    assert fetched.building.address == building.address
    assert len(fetched.categories) == 3
    eat_category = next(category for category in fetched.categories if category.name == eat.name)
    assert len(eat_category.subcategories) == 1
    assert len(eat_category.subcategories[0].subcategories) == 1
    assert eat_category.subcategories[0].subcategories[0].id == cheese.id
    assert len(fetched.phones) == 1
    assert fetched.phones[0].id == phone.id


@pytest.mark.asyncio
async def test_get_by_building_id(async_session, create_building, create_organization):
    building1 = await create_building("ул. Тестовая, д.1", 54.8776, 20.3145)
    org1 = await create_organization("ООО Тест", building1.id)
    org2 = await create_organization("ОАО Прод", building1.id)
    building2 = await create_building("ул. Продовая, д.7", 54.6543, 20.9087)
    org3 = await create_organization("ЗАО Собес", building2.id)

    repo = OrganizationRepository(async_session)
    result = await repo.get_by_building_id(building1.id)

    assert len(result) == 2
    names = [org.name for org in result]
    assert org1.name in names and org2.name in names
    assert org3.name not in names


@pytest.mark.asyncio
async def test_get_by_category_id(async_session, create_category, create_organization):
    eat = await create_category("Еда")
    milk = await create_category("Молочная продукция", base_category_id=eat.id)
    org1 = await create_organization("ООО Тест", category_ids=[eat.id, milk.id])
    org2 = await create_organization("ОАО Прод", category_ids=[eat.id])
    furniture = await create_category("Мебель")
    org3 = await create_organization("ЗАО Собес", category_ids=[furniture.id])

    repo = OrganizationRepository(async_session)
    result = await repo.get_by_category_id(eat.id)

    assert len(result) == 2
    assert all(any(category.name == eat.name for category in organization.categories) for organization in result)
    org_ids = [organization.id for organization in result]
    assert org1.id in org_ids and org3.id in org_ids
    assert org2.id not in org_ids


@pytest.mark.asyncio
async def test_search_by_name(async_session, create_organization):
    org1 = await create_organization("ООО Тест Задание")
    org2 = await create_organization("ЗАО Тест Здание")
    org3 = await create_organization("ОАО Прод Задание")

    repo = OrganizationRepository(async_session)
    result = await repo.search_by_name("прод")

    assert len(result) == 1
    assert result[0].name == org3.name

    result = await repo.search_by_name("задание")
    assert len(result) == 2
    org_ids = [organization.id for organization in result]
    assert org1.id in org_ids and org3.id in org_ids
    assert org2.id not in org_ids
