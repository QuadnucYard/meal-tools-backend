from __future__ import annotations

from .base import OrmModel


class CanteenBase(OrmModel):
    name: str
    aliases: list[str]


class CanteenCreate(CanteenBase):
    ...


class CanteenRead(CanteenBase):
    id: int
