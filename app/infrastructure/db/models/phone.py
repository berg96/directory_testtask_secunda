from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.db.base import Base

if TYPE_CHECKING:
    from .organization import Organization


class Phone(Base):
    phone: Mapped[str] = mapped_column(String(20), nullable=False, comment="Номер телефона")
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"))

    organization: Mapped["Organization"] = relationship("Organization", back_populates="phones")
