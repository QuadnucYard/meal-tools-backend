from typing import Any, Type, TypeVar, overload

from pydantic import BaseModel

from app.db.session import AsyncEngine, AsyncSession
from app.models.base import Base

SchemaType = TypeVar("SchemaType", bound=BaseModel)
ModelType = TypeVar("ModelType", bound=Base)


@overload
async def from_orm_async(
    db: AsyncSession, model: Type[SchemaType], obj: ModelType, update: dict[str, Any] | None = None
) -> SchemaType:
    ...


@overload
async def from_orm_async(
    db: AsyncSession,
    model: Type[SchemaType],
    obj: list[ModelType],
    update: dict[str, Any] | None = None,
) -> list[SchemaType]:
    ...


async def from_orm_async(
    db: AsyncSession,
    model: Type[SchemaType],
    obj: ModelType | list[ModelType],
    update: dict[str, Any] | None = None,
) -> SchemaType | list[SchemaType]:
    if isinstance(obj, list):
        return await db.run_sync(lambda _: [model.model_validate(obj_) for obj_ in obj])
    else:
        return await db.run_sync(lambda _: model.model_validate(obj))


class no_echo:
    def __init__(self, engine: AsyncEngine) -> None:
        self.engine = engine
        self.echo = self.engine.echo

    def __enter__(self):
        self.echo = self.engine.echo
        self.engine.echo = False

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.engine.echo = self.echo
