from collections import defaultdict
from typing import Optional

from app.infrastructure.db import Category


class CategoryEntity:
    def __init__(
        self,
        id: int,
        name: str,
        base_category_id: Optional[int] = None,
        subcategories: Optional[list["CategoryEntity"]] = None,
    ):
        self.id = id
        self.name = name
        self.base_category_id = base_category_id
        self.subcategories = subcategories or []

    def add_subcategory(self, subcategory: "CategoryEntity"):
        self.subcategories.append(subcategory)

    @classmethod
    def from_orm(cls, orm_obj: Category) -> "CategoryEntity":
        return cls(
            id=orm_obj.id,
            name=orm_obj.name,
            base_category_id=getattr(orm_obj, "base_category_id", None),
            subcategories=[],
        )

    @classmethod
    def _build_tree(cls, categories: list[Category]) -> tuple[list["CategoryEntity"], dict[int, "CategoryEntity"]]:
        entities = {category.id: cls.from_orm(category) for category in categories}
        tree = defaultdict(list)
        for category in categories:
            if category.base_category_id in entities:
                tree[category.base_category_id].append(entities[category.id])

        for parent_id, children in tree.items():
            entities[parent_id].subcategories.extend(children)

        roots = [e for e in entities.values() if e.base_category_id not in entities]

        return roots, entities

    @classmethod
    def get_roots_of_category_tree(cls, categories: list[Category]) -> list["CategoryEntity"]:
        return cls._build_tree(categories)[0]

    @classmethod
    def get_categories_with_nested_categories(cls, categories: list[Category]) -> list["CategoryEntity"]:
        return list(cls._build_tree(categories)[1].values())
