from types import SimpleNamespace
from typing import Optional

import pytest


@pytest.fixture
def create_category_orm():
    def _create(id: int, name: str, base_category_id: Optional[int] = None) -> SimpleNamespace:
        return SimpleNamespace(id=id, name=name, base_category_id=base_category_id)

    return _create


@pytest.fixture
def few_category_orm(create_category_orm):
    return [
        create_category_orm(1, "Еда"),
        create_category_orm(2, "Молочная продукция", base_category_id=1),
        create_category_orm(3, "Сыры", base_category_id=2),
        create_category_orm(4, "Мясная продукция", base_category_id=1),
        create_category_orm(5, "Мебель"),
        create_category_orm(6, "Кровать", base_category_id=5),
    ]


@pytest.fixture
def create_building_orm():
    def _create(id: int, address: str, latitude: float, longitude: float) -> SimpleNamespace:
        return SimpleNamespace(id=id, address=address, latitude=latitude, longitude=longitude)

    return _create


@pytest.fixture
def create_phone_orm():
    def _create(id: int, number: str) -> SimpleNamespace:
        return SimpleNamespace(id=id, number=number)

    return _create


@pytest.fixture
def create_organization_orm(create_building_orm, create_phone_orm, few_category_orm):
    def _create(
        id: int,
        name: str,
        phones: Optional[list[SimpleNamespace]] = None,
        building: Optional[SimpleNamespace] = None,
        categories: Optional[list[SimpleNamespace]] = None,
    ) -> SimpleNamespace:
        return SimpleNamespace(
            id=id,
            name=name,
            phones=phones or [create_phone_orm(1, "+7 (999) 123-45-67")],
            building=building or create_building_orm(1, "ул. Тестовая, д.1", 54.8776, 20.3145),
            # По умолчанию "Молочная продукция", "Сыры" и "Кровать"
            categories=categories or [few_category_orm[1], few_category_orm[2], few_category_orm[5]],
        )

    return _create
