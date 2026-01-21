import pytest

from app.domain.entities import CategoryEntity
from app.infrastructure.db.repositories.category import CategoryRepository


@pytest.mark.asyncio
async def test_get_category_with_nested_categories(create_category, async_session):
    eat = await create_category("Еда")
    milk = await create_category("Молочная продукция", base_category_id=eat.id)
    meat = await create_category("Мясная продукция", base_category_id=eat.id)
    cheese = await create_category("Сыры", base_category_id=milk.id)
    repo = CategoryRepository(session=async_session)

    result = await repo.get_category_with_nested_categories(eat.id, max_depth=2)
    assert all(isinstance(category, CategoryEntity) for category in result)
    eat_entity = next(category for category in result if category.name == eat.name)
    assert len(eat_entity.subcategories) == 2
    assert any(category.name == meat.name for category in result)
    assert all(category.name != cheese.name for category in result)

    result = await repo.get_category_with_nested_categories(eat.id)
    assert len(result) == 4
    assert any(category.name == cheese.name for category in result)
    eat_entity = next(category for category in result if category.name == eat.name)
    milk_entity = next(category for category in eat_entity.subcategories if category.name == milk.name)
    assert len(milk_entity.subcategories) == 1
    assert milk_entity.subcategories[0].name == cheese.name

    result = await repo.get_category_with_nested_categories(milk.id)
    assert len(result) == 2
