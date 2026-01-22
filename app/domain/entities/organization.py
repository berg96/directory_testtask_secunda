from typing import Optional

from app.domain.entities.building import BuildingEntity
from app.domain.entities.category import CategoryEntity
from app.domain.entities.phone import PhoneEntity
from app.infrastructure.db import Organization


class OrganizationEntity:
    def __init__(
        self,
        id: int,
        name: str,
        phones: list[PhoneEntity],
        building: Optional[BuildingEntity],
        categories: list[CategoryEntity],
    ):
        self.id = id
        self.name = name
        self.phones = phones
        self.building = building
        self.categories = categories

    @classmethod
    def from_orm(cls, orm_obj: Organization) -> "OrganizationEntity":
        building_obj = getattr(orm_obj, "building", None)
        categories = getattr(orm_obj, "categories", [])
        return cls(
            id=orm_obj.id,
            name=orm_obj.name,
            phones=[PhoneEntity.from_orm(phone) for phone in getattr(orm_obj, "phones", [])],
            building=BuildingEntity.from_orm(building_obj) if building_obj else None,
            categories=CategoryEntity.get_categories_with_nested_categories(categories) if categories else [],
        )
