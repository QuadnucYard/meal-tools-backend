from .base import OrmModel, TimeMixin


class TagBase(OrmModel):
    name: str
    category: str | None = None
    color: str


class TagCreate(TagBase):
    ...


class TagUpdate(TagBase):
    ...


class TagRead(TagBase, TimeMixin):
    id: int


class TagReadWithFoods(TagRead):
    food_ids: list[int]


__all__ = ["TagBase", "TagCreate", "TagUpdate", "TagRead", "TagReadWithFoods"]
