from app.domain.entities import OrganizationEntity


def test_organization_from_orm(create_organization_orm):
    org_id = 1
    org_name = "ООО Тест"
    orm = create_organization_orm(org_id, org_name)
    entity = OrganizationEntity.from_orm(orm)
    assert entity.id == orm.id == org_id
    assert entity.name == orm.name == org_name
    assert entity.building.address == orm.building.address
    assert entity.phones[0].number == orm.phones[0].number
    assert len(entity.categories) == len(orm.categories) == 3
    assert "Молочная продукция" in [category.name for category in entity.categories]
