import json

from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, int_pk


class Canteen(Base):
    id: Mapped[int_pk]
    name: Mapped[str]
    _aliases: Mapped[str] = mapped_column("aliases")
    desc: Mapped[str]

    @property
    def aliases(self) -> list[str]:
        return json.loads(self._aliases)

    @aliases.setter
    def aliases(self, aliases: list[str]):
        self._aliases = json.dumps(aliases, ensure_ascii=False)


__all__ = ["Canteen"]
