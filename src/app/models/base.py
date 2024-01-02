from datetime import datetime
from typing import Annotated

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

int_pk = Annotated[int, mapped_column(primary_key=True)]
str_pk = Annotated[str, mapped_column(primary_key=True)]
str_uid = Annotated[str, mapped_column(index=True, unique=True)]
str_idx = Annotated[str, mapped_column(index=True)]
datetime_def = Annotated[datetime, mapped_column(default=func.now())]


class Base(AsyncAttrs, DeclarativeBase):
    def __init_subclass__(cls, *, tablename: str | None = None) -> None:
        cls.__tablename__ = tablename or cls.__name__.lower()
        return super().__init_subclass__()


class TimeMixin:
    create_time: Mapped[datetime] = mapped_column(default=func.now())
    update_time: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())
