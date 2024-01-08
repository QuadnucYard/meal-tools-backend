import json
from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .assoc import FoodTagLink
from .base import Base, TimeMixin

if TYPE_CHECKING:
    from .tag import Tag


class Food(TimeMixin, Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("food.id"), default=None)
    name: Mapped[str]
    _aliases: Mapped[str] = mapped_column("aliases")
    price: Mapped[int]
    desc: Mapped[str]
    _images: Mapped[str] = mapped_column("images")

    parent: Mapped[Optional["Food"]] = relationship("Food", back_populates="variants", remote_side=[id])
    variants: Mapped[list["Food"]] = relationship("Food", back_populates="parent")
    tags: Mapped[list["Tag"]] = relationship(secondary=FoodTagLink, back_populates="foods")

    @property
    def aliases(self) -> list[str]:
        return json.loads(self._aliases)

    @aliases.setter
    def aliases(self, aliases: list[str]):
        self._aliases = json.dumps(aliases)

    @property
    def images(self) -> list[str]:
        return json.loads(self._images)

    @images.setter
    def images(self, images: list[str]):
        self._images = json.dumps(images)
