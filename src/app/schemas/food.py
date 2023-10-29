from __future__ import annotations

from datetime import datetime

from .base import OrmModel


class FoodBase(OrmModel):
    name: str
    aliases: list[str]
    price: int
    desc: str


class FoodCreate(FoodBase):
    ...


class FoodRead(FoodBase):
    id: int
    create_time: datetime
