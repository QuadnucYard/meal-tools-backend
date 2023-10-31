from __future__ import annotations

from datetime import date, datetime

from .base import OrmModel


class WeighBase(OrmModel):
    canteen_id: int
    food_id: int
    weight: int
    record_date: date


class WeighCreate(WeighBase):
    ...


class WeighRead(WeighBase):
    id: int
    create_time: datetime


class WeighUpdate(OrmModel):
    canteen_id: int | None = None
    food_id: int | None = None
    weight: int | None = None
    record_date: date | None = None


__all__ = ["WeighCreate", "WeighRead", "WeighUpdate"]
