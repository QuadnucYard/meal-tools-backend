from __future__ import annotations

from typing import TYPE_CHECKING

from .base import OrmModel, TimeMixin

if TYPE_CHECKING:
    from app.schemas.food import FoodRead


class TagBase(OrmModel):
    name: str
    category: str | None
    color: str


class TagCreate(TagBase):
    ...


class TagUpdate(TagBase):
    ...


class TagRead(TagBase, TimeMixin):
    id: int


class TagReadWithFoods(TagRead):
    foods: list[FoodRead]


__all__ = ["TagBase", "TagCreate", "TagUpdate", "TagRead", "TagReadWithFoods"]
