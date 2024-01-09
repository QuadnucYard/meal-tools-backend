from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, subqueryload

from app.crud.base import CRUDBase
from app.models.food import Food
from app.models.weigh import Weigh


class CRUDFood(CRUDBase[Food, BaseModel, BaseModel]):
    async def get_x(self, db: AsyncSession, id: int):
        return await self.get(db, id, options=(selectinload(Food.tags), selectinload(Food.variants)))

    async def get_with_weight(self, db: AsyncSession):
        subq = (
            select(
                Weigh.food_id,
                func.count().label("weight_cnt"),
                func.avg(Weigh.weight).label("weight_avg"),
                func.sqrt(
                    func.avg(Weigh.weight * Weigh.weight) - func.avg(Weigh.weight) * func.avg(Weigh.weight)
                ).label("weight_std"),
            )
            .group_by(Weigh.food_id)
            .subquery()
        )
        stmt = (
            select(Food, subq.c.weight_cnt, subq.c.weight_avg, subq.c.weight_std)
            .join_from(Food, subq)
            .options(subqueryload(Food.tags), subqueryload(Food.variants))
        )
        return list((await db.execute(stmt)).all())


food = CRUDFood(Food)
