from app.domain.entities import CategoryEntity


def test_get_roots_of_category_tree(few_category_orm):
    root = next(c for c in CategoryEntity.get_roots_of_category_tree(few_category_orm) if c.name == "Еда")
    assert root.name == "Еда"
    assert len(root.subcategories) == 2
    milk = next(c for c in root.subcategories if c.name == "Молочная продукция")
    assert len(milk.subcategories) == 1
    assert milk.subcategories[0].name == "Сыры"


def test_get_categories_with_nested_categories(few_category_orm):
    categories = CategoryEntity.get_categories_with_nested_categories(few_category_orm)
    assert len(categories) == len(few_category_orm)
    eat = next(c for c in categories if c.name == "Еда")
    assert len(eat.subcategories) == 2
