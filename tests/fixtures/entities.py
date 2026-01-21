from typing import Optional

import pytest

from app.domain.entities import BuildingEntity, CategoryEntity, OrganizationEntity, PhoneEntity


@pytest.fixture
def create_category_entity():
    def _create(
        id: int,
        name: str,
        base_category_id: Optional[int] = None,
        subcategories: Optional[list["CategoryEntity"]] = None,
    ) -> CategoryEntity:
        return CategoryEntity(id, name, base_category_id, subcategories)

    return _create


@pytest.fixture
def few_categories(create_category_entity) -> list[CategoryEntity]:
    eat = create_category_entity(1, "Еда")
    milk = create_category_entity(2, "Молочная продукция", base_category_id=1)
    eat.subcategories.append(milk)
    meat = create_category_entity(3, "Мясная продукция", base_category_id=1)
    eat.subcategories.append(meat)
    cheese = create_category_entity(4, "Сыры", base_category_id=2)
    milk.subcategories.append(cheese)
    furniture = create_category_entity(5, "Мебель")
    bed = create_category_entity(6, "Кровать", base_category_id=5)
    furniture.subcategories.append(bed)
    return [eat, milk, meat, cheese, furniture, bed]


@pytest.fixture
def create_building_entity():
    def _create(id: int, address: str, latitude: float, longitude: float) -> BuildingEntity:
        return BuildingEntity(id, address, latitude, longitude)

    return _create


@pytest.fixture
def create_phone_entity():
    def _create(id: int, number: str) -> PhoneEntity:
        return PhoneEntity(id, number)

    return _create


@pytest.fixture
def create_organization_entity(create_building_entity, create_phone_entity, few_categories):
    def _create(
        id: int,
        name: str,
        phones: Optional[list[PhoneEntity]] = None,
        building: Optional[BuildingEntity] = None,
        categories: Optional[list[CategoryEntity]] = None,
    ) -> OrganizationEntity:
        return OrganizationEntity(
            id=id,
            name=name,
            phones=phones or [create_phone_entity(1, "+7 (999) 123-45-67")],
            building=building or create_building_entity(1, "ул. Тестовая, д.1", 54.8776, 20.3145),
            # По умолчанию "Молочная продукция", "Сыры" и "Кровать"
            categories=categories or [few_categories[1], few_categories[3], few_categories[5]],
        )

    return _create
