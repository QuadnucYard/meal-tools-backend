import json

from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, datetime_def, int_pk


class Food(Base):
    id: Mapped[int_pk]
    name: Mapped[str]
    _aliases: Mapped[str] = mapped_column("aliases")
    price: Mapped[int]
    desc: Mapped[str]
    create_time: Mapped[datetime_def]

    @property
    def aliases(self) -> list[str]:
        return json.loads(self._aliases)

    @aliases.setter
    def aliases(self, aliases: list[str]):
        self._aliases = json.dumps(aliases)


__all__ = ["Food"]
