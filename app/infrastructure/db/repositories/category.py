from typing import Optional

from sqlalchemy import literal, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.settings import settings
from app.domain.entities.category import CategoryEntity
from app.infrastructure.db import Category


class CategoryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def exists(self, category_id: int) -> bool:
        query = select(Category.id).where(Category.id == category_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none() is not None

    async def get_category_with_nested_categories(
        self,
        category_id: int,
        max_depth: Optional[int] = settings.CATEGORY_MAX_DEPTH,
    ) -> list[CategoryEntity]:
        """
        Возвращает категорию + всех потомков до max_depth
        """
        cte = (
            select(
                Category,
                literal(1).label("depth"),
            )
            .where(Category.id == category_id)
            .cte(name="nested_categories", recursive=True)
        )

        recursive = select(
            Category,
            (cte.c.depth + 1).label("depth"),
        ).where(Category.base_category_id == cte.c.id)

        if max_depth is not None:
            recursive = recursive.where(cte.c.depth < max_depth)

        cte = cte.union_all(recursive)
        query = select(Category).join(cte, Category.id == cte.c.id)
        result = await self.session.execute(query)
        return CategoryEntity.get_categories_with_nested_categories(list(result.scalars().all()))
