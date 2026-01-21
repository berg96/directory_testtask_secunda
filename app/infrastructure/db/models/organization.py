from typing import TYPE_CHECKING, Optional

from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.db.base import Base

from .building import Building
from .phone import Phone

if TYPE_CHECKING:
    from .category import Category

organization_category = Table(
    "organization_category",
    Base.metadata,
    Column("organization_id", ForeignKey("organizations.id", ondelete="CASCADE"), primary_key=True),
    Column("category_id", ForeignKey("categories.id", ondelete="CASCADE"), primary_key=True),
)


class Organization(Base):
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, comment="Название организации")
    building_id: Mapped[Optional[int]] = mapped_column(ForeignKey("buildings.id", ondelete="SET NULL"))

    building: Mapped[Building] = relationship(Building, back_populates="organizations")
    categories: Mapped[list["Category"]] = relationship(
        "Category", secondary=organization_category, back_populates="organizations"
    )
    phones: Mapped[list[Phone]] = relationship(Phone, back_populates="organization", cascade="all, delete-orphan")
