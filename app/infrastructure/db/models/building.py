from typing import TYPE_CHECKING

from geoalchemy2 import Geography
from sqlalchemy import Float, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.db.base import Base

if TYPE_CHECKING:
    from .organization import Organization


class Building(Base):
    address: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, comment="Адрес здания")
    latitude: Mapped[float] = mapped_column(Float, nullable=False, comment="Широта")
    longitude: Mapped[float] = mapped_column(Float, nullable=False, comment="Долгота")
    location: Mapped[str] = mapped_column(Geography(geometry_type="POINT", srid=4326), nullable=False)

    organizations: Mapped[list["Organization"]] = relationship("Organization", back_populates="building")

    __table_args__ = (UniqueConstraint("latitude", "longitude", name="uq_building_lat_lon"),)
