from pydantic import BaseModel, Field

from app.domain.entities import PhoneEntity


class PhoneResponse(BaseModel):
    id: int = Field(..., description="Идентификатор записи телефона в БД")
    number: str = Field(..., description="Номер телефона")

    @classmethod
    def from_entity(cls, entity: PhoneEntity) -> "PhoneResponse":
        return cls(id=entity.id, number=entity.number)
