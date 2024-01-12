from __future__ import annotations

from .base import OrmModel, TimeMixin

# if TYPE_CHECKING:
from .tag import TagRead


class FoodBase(OrmModel):
    parent_id: int | None = None
    name: str
    aliases: list[str]
    price: int
    desc: str
    images: list[str]


class FoodCreate(FoodBase):
    ...


class FoodUpdate(OrmModel):
    name: str | None = None
    aliases: list[str] | None = None
    price: int | None = None
    desc: str | None = None
    images: list[str] | None = None


class FoodRead(FoodBase, TimeMixin):
    id: int


class FoodReadWithVariants(FoodRead):
    variants: list[FoodReadWithVariants]
    tags: list[TagRead]


class FoodStats(OrmModel):
    weight_cnt: int
    weight_avg: float
    weight_std: float


class FoodReadWithStats(FoodReadWithVariants, FoodStats):
    ...


__all__ = ["FoodCreate", "FoodRead", "FoodReadWithVariants", "FoodReadWithStats", "FoodUpdate"]
