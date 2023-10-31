from __future__ import annotations

from datetime import datetime

from .base import OrmModel


class FoodBase(OrmModel):
    parent_id: int | None
    name: str
    aliases: list[str]
    price: int
    desc: str
    image: str | None


class FoodCreate(FoodBase):
    ...


class FoodRead(FoodBase):
    id: int
    create_time: datetime


class FoodReadWithVariants(FoodRead):
    variants: list[FoodReadWithVariants]


class FoodUpdate(OrmModel):
    name: str | None = None
    aliases: list[str] | None = None
    price: int | None = None
    desc: str | None = None
    image: str | None = None


__all__ = ["FoodCreate", "FoodRead", "FoodReadWithVariants", "FoodUpdate"]
