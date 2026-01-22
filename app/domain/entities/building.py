from app.infrastructure.db import Building


class BuildingEntity:
    def __init__(
        self,
        id: int,
        address: str,
        latitude: float,
        longitude: float,
    ):
        self.id = id
        self.address = address
        self.latitude = latitude
        self.longitude = longitude

    @classmethod
    def from_orm(cls, orm_obj: Building) -> "BuildingEntity":
        return cls(
            id=orm_obj.id,
            address=orm_obj.address,
            latitude=orm_obj.latitude,
            longitude=orm_obj.longitude,
        )
