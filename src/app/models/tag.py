from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from .assoc import FoodTagLink
from .base import Base, int_pk

if TYPE_CHECKING:
    from .food import Food


class Tag(Base):
    id: Mapped[int_pk]
    name: Mapped[str]

    foods: Mapped[list["Food"]] = relationship(secondary=FoodTagLink, back_populates="tags", lazy="raise")
