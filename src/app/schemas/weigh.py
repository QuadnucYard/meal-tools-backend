from __future__ import annotations

from datetime import date

from .base import OrmModel, TimeMixin


class WeighBase(OrmModel):
    canteen_id: int
    food_id: int
    weight: int
    record_date: date


class WeighCreate(WeighBase):
    image: str | None = None


class WeighRead(WeighBase, TimeMixin):
    id: int
    image: str | None


class WeighUpdate(OrmModel):
    canteen_id: int | None = None
    food_id: int | None = None
    weight: int | None = None
    record_date: date | None = None
    image: str | None = None


__all__ = ["WeighCreate", "WeighRead", "WeighUpdate"]
