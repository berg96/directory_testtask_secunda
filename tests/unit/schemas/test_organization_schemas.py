from app.api.schemas.organization import OrganizationListResponse, OrganizationResponse


def test_organization_response_from_entity(
    create_building_entity, create_phone_entity, create_category_entity, create_organization_entity
):
    eat = create_category_entity(1, "Еда")
    milk = create_category_entity(2, "Молочная продукция", base_category_id=1)
    furniture = create_category_entity(3, "Мебель")
    building = create_building_entity(1, "ул. Тестовая, д.1", 54.8776, 20.3145)
    phone = create_phone_entity(1, "+7 (999) 123-45-67")
    organization = create_organization_entity(
        id=1, name="ООО Тест", phones=[phone], building=building, categories=[eat, milk, furniture]
    )

    result = OrganizationResponse.from_entity(organization)

    assert result.id == organization.id == 1
    assert result.name == organization.name == "ООО Тест"

    assert result.building is not None
    assert result.building.id == building.id == 1

    assert result.phones is not None
    assert len(result.phones) == 1
    assert result.phones[0].id == phone.id == 1

    assert result.categories is not None
    assert len(result.categories) == 3
    category_ids = [category.id for category in result.categories]
    assert eat.id in category_ids and milk.id in category_ids and furniture.id in category_ids


def test_organization_list_response_multiple_items(create_organization_entity):
    organization1 = create_organization_entity(id=1, name="ООО Тест")
    organization2 = create_organization_entity(id=2, name="ОАО Прод")

    result = OrganizationListResponse.from_entities([organization1, organization2])

    assert result.count == 2
    assert len(result.items) == 2
    assert result.items[0].id == organization1.id == 1
    assert result.items[1].id == organization2.id == 2
