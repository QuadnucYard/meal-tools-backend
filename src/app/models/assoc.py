from typing import Final

from sqlalchemy import Column, ForeignKey, Table

from .base import Base

FoodTagLink: Final[Table] = Table(
    "food_tag_link",
    Base.metadata,
    Column("food_id", ForeignKey("food.id"), primary_key=True),
    Column("tag_id", ForeignKey("tag.id"), primary_key=True),
)
