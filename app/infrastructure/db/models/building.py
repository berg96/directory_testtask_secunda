from sqlalchemy import Float, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.db.base import Base


class Building(Base):
    address: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, comment="Адрес здания")
    latitude: Mapped[float] = mapped_column(Float, nullable=False, comment="Широта")
    longitude: Mapped[float] = mapped_column(Float, nullable=False, comment="Долгота")

    organizations: Mapped[list] = relationship("Organization", back_populates="building")

    __table_args__ = (UniqueConstraint("latitude", "longitude", name="uq_building_lat_lon"),)
