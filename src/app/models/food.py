import json
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, datetime_def


class Food(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("food.id"), default=None)
    name: Mapped[str]
    _aliases: Mapped[str] = mapped_column("aliases")
    price: Mapped[int]
    desc: Mapped[str]
    image: Mapped[str | None] = mapped_column(default=None)
    create_time: Mapped[datetime_def]

    parent: Mapped[Optional["Food"]] = relationship("Food", back_populates="variants", remote_side=[id])
    variants: Mapped[list["Food"]] = relationship("Food", back_populates="parent")
    # variants: Mapped[list["Food"]] = relationship("Food")

    @property
    def aliases(self) -> list[str]:
        return json.loads(self._aliases)

    @aliases.setter
    def aliases(self, aliases: list[str]):
        self._aliases = json.dumps(aliases)


__all__ = ["Food"]
