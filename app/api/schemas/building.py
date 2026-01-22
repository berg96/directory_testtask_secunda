from pydantic import BaseModel, Field

from app.domain.entities import BuildingEntity


class BuildingResponse(BaseModel):
    id: int = Field(..., description="Идентификатор здания")
    address: str = Field(..., description="Адрес здания")
    latitude: float = Field(..., description="Широта")
    longitude: float = Field(..., description="Долгота")

    @classmethod
    def from_entity(cls, entity: BuildingEntity) -> "BuildingResponse":
        return cls(
            id=entity.id,
            address=entity.address,
            latitude=entity.latitude,
            longitude=entity.longitude,
        )


class BuildingListResponse(BaseModel):
    count: int = Field(..., description="Количество зданий")
    items: list[BuildingResponse] = Field(..., description="Список зданий")

    @classmethod
    def from_entities(cls, entities: list[BuildingEntity]):
        return cls(
            count=len(entities),
            items=[BuildingResponse.from_entity(e) for e in entities],
        )
