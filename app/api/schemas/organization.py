from typing import Optional

from pydantic import BaseModel, Field

from ...domain.entities import OrganizationEntity
from .building import BuildingResponse
from .category import CategoryResponse
from .phone import PhoneResponse


class OrganizationResponse(BaseModel):
    id: int = Field(..., description="Идентификатор организации")
    name: str = Field(..., description="Название организации")
    building: Optional[BuildingResponse] = Field(None, description="Здание, в котором находится организация")
    phones: Optional[list[PhoneResponse]] = Field(None, description="Список телефонов организации")
    categories: Optional[list[CategoryResponse]] = Field(None, description="Список деятельностей организации")

    @classmethod
    def from_entity(cls, entity: OrganizationEntity) -> "OrganizationResponse":
        return cls(
            id=entity.id,
            name=entity.name,
            building=BuildingResponse.from_entity(entity.building) if entity.building else None,
            phones=[PhoneResponse.from_entity(phone) for phone in entity.phones] if entity.phones else None,
            categories=(
                [CategoryResponse.from_entity(category) for category in entity.categories]
                if entity.categories
                else None
            ),
        )


class OrganizationListResponse(BaseModel):
    count: int = Field(..., description="Количество организаций")
    items: list[OrganizationResponse] = Field(..., description="Список организаций")

    @classmethod
    def from_entities(cls, entities: list[OrganizationEntity]):
        return cls(
            count=len(entities),
            items=[OrganizationResponse.from_entity(e) for e in entities],
        )
