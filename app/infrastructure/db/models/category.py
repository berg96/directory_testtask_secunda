from typing import Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.db.base import Base


class Category(Base):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True, comment="Название категории (деятельности)"
    )
    base_category_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("categories.id"), nullable=True, comment="ID базовой категории (родителя)"
    )

    base_category: Mapped["Category"] = relationship("Category", remote_side=[Base.id], backref="subcategories")
    organizations: Mapped[list] = relationship(
        "Organization", secondary="organization_category", back_populates="categories"
    )
