from __future__ import annotations

from typing import TYPE_CHECKING, Any, Generic, Sequence, Type, TypedDict, TypeVar

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi_pagination import Page
from fastapi_pagination.ext.async_sqlalchemy import paginate
from fastapi_pagination.types import AsyncItemsTransformer
from pydantic import BaseModel
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.inspection import inspect

from app.models.base import Base

if TYPE_CHECKING:
    from app.schemas.page import PageParams

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class DateCount(TypedDict):
    date: str
    count: int


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    async def get(self, db: AsyncSession, id: Any) -> ModelType | None:
        return await db.get(self.model, id)

    async def get_if(self, db: AsyncSession, *where_clause) -> ModelType | None:
        stmt = select(self.model).where(*where_clause)
        return await db.scalar(stmt)

    async def get_one(self, db: AsyncSession, id: Any) -> ModelType:
        ret = await self.get(db, id)
        if not ret:
            raise HTTPException(404, f"Not found {self.model.__name__} with id {id}")
        return ret

    async def get_ones(self, db: AsyncSession, ids: Sequence[Any]) -> list[ModelType]:
        return [await self.get_one(db, id) for id in ids]

    async def get_ones_unordered(self, db: AsyncSession, ids: Sequence[Any], pk: Any) -> list[ModelType]:
        stmt = select(self.model).filter(pk.in_(ids))
        return list((await db.scalars(stmt)).all())

    async def get_many(self, db: AsyncSession, *, offset: int = 0, limit: int = 100) -> list[ModelType]:
        stmt = select(self.model).offset(offset).limit(limit)
        return list((await db.scalars(stmt)).all())

    async def get_page(
        self,
        db: AsyncSession,
        *,
        page: PageParams,
        transformer: AsyncItemsTransformer | None = None,
    ) -> Page:
        stmt = select(self.model)
        if page.sort_by:
            key = getattr(self.model, page.sort_by)
            key = desc(key) if page.desc else key
            stmt = stmt.order_by(key)
        return await paginate(db, stmt, transformer=transformer)

    async def get_page_if(
        self,
        db: AsyncSession,
        *where_clause,
        page: PageParams,
        transformer: AsyncItemsTransformer | None = None,
    ) -> Page:
        stmt = select(self.model).where(*where_clause)
        if page.sort_by:
            key = getattr(self.model, page.sort_by)
            key = desc(key) if page.desc else key
            stmt = stmt.order_by(key)
        return await paginate(db, stmt, transformer=transformer)

    async def add(self, db: AsyncSession, db_obj: ModelType):
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def adds(self, db: AsyncSession, db_objs: Sequence[ModelType]):
        db.add_all(db_objs)
        await db.commit()
        for db_obj in db_objs:
            await db.refresh(db_obj)
        return db_objs

    async def create(self, db: AsyncSession, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in.model_dump())
        return await self.add(db, db_obj)

    async def update(
        self, db: AsyncSession, *, db_obj: ModelType, obj_in: UpdateSchemaType | dict[str, Any]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in if isinstance(obj_in, dict) else obj_in.model_dump(exclude_unset=True, exclude_none=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        return await self.add(db, db_obj)

    async def upsert(self, db: AsyncSession, obj_in: dict[str, Any]):
        pk = [obj_in[k.name] for k in inspect(self.model).primary_key]
        db_obj = await db.get(self.model, pk)
        if db_obj:
            return await self.update(db, db_obj=db_obj, obj_in=obj_in)
        db_obj = self.model(**obj_in)
        return await self.add(db, db_obj)

    async def delete(self, db: AsyncSession, db_obj: ModelType):
        await db.delete(db_obj)
        await db.commit()
        return db_obj

    async def remove(self, db: AsyncSession, *, id: Any) -> ModelType:
        obj = await db.get(self.model, id)
        assert obj
        return await self.delete(db, obj)
