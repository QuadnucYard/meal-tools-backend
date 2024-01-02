from datetime import date, datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimeMixin, int_pk

if TYPE_CHECKING:
    from .canteen import Canteen
    from .food import Food


class Weigh(TimeMixin, Base):
    id: Mapped[int_pk]
    canteen_id: Mapped[int] = mapped_column(ForeignKey("canteen.id"), default=None)
    food_id: Mapped[int] = mapped_column(ForeignKey("food.id"), default=None)
    weight: Mapped[float]
    _record_date: Mapped[datetime] = mapped_column("record_date")
    image: Mapped[str | None] = mapped_column(default=None)

    canteen: Mapped["Canteen"] = relationship()
    food: Mapped["Food"] = relationship()

    @property
    def record_date(self) -> date:
        return self._record_date.date()

    @record_date.setter
    def record_date(self, date: date):
        self._record_date = datetime(date.year, date.month, date.day)


__all__ = ["Weigh"]
