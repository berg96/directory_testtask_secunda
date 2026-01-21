from typing import Optional

from pydantic import BaseModel, Field

from app.domain.entities import CategoryEntity


class CategoryResponse(BaseModel):
    id: int = Field(..., description="Идентификатор деятельности")
    name: str = Field(..., description="Название деятельности")
    base_category_id: Optional[int] = Field(None, description="Идентификатор деятельности-родителя")
    subcategories: Optional[list["CategoryResponse"]] = Field(None, description="Список деятельностей-потомков")

    @classmethod
    def from_entity(cls, entity: CategoryEntity) -> "CategoryResponse":
        return cls(
            id=entity.id,
            name=entity.name,
            base_category_id=entity.base_category_id or None,
            subcategories=(
                [cls.from_entity(subcategory) for subcategory in entity.subcategories] if entity.subcategories else None
            ),
        )
