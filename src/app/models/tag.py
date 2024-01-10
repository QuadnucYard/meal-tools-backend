from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .assoc import FoodTagLink
from .base import Base, TimeMixin, int_pk

if TYPE_CHECKING:
    from .food import Food


class Tag(TimeMixin, Base):
    id: Mapped[int_pk]
    name: Mapped[str] = mapped_column(unique=True, index=True)
    category: Mapped[str | None] = mapped_column(default=None)
    color: Mapped[str] = mapped_column(server_default="grey")

    foods: Mapped[list["Food"]] = relationship(secondary=FoodTagLink, back_populates="tags", lazy="raise")
