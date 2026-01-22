from app.infrastructure.db import Phone


class PhoneEntity:
    def __init__(self, id: int, number: str):
        self.id = id
        self.number = number

    @classmethod
    def from_orm(cls, orm_obj: Phone) -> "PhoneEntity":
        return cls(
            id=orm_obj.id,
            number=orm_obj.number,
        )
