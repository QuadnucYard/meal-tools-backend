from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.crud.base import CRUDBase
from app.models.food import Food
from app.models.weigh import Weigh


class CRUDFood(CRUDBase[Food, BaseModel, BaseModel]):
    async def get_x(self, db: AsyncSession, id: int):
        return await self.get(db, id, options=(joinedload(Food.tags), joinedload(Food.variants)))

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
        stmt = select(Food, subq.c.weight_cnt, subq.c.weight_avg, subq.c.weight_std).join_from(Food, subq)
        # subq = (
        #     select(
        #         Weigh.food_id,
        #         func.count().label("weight_cnt"),
        #         func.avg(Weigh.weight).label("weight_avg"),
        #         func.avg(Weigh.weight * Weigh.weight).label("weight_sqr"),
        #     )
        #     .group_by(Weigh.food_id)
        #     .cte()
        # )
        # subq2 = select(
        #     subq.c.food_id,
        #     subq.c.weight_cnt,
        #     subq.c.weight_avg,
        #     func.sqrt(subq.c.weight_sqr - subq.c.weight_avg * subq.c.weight_avg).label("weight_std"),
        # ).subquery()
        # stmt = select(Food, subq2.c.weight_cnt, subq2.c.weight_avg, subq2.c.weight_std).join_from(Food, subq)
        return list((await db.execute(stmt)).all())


food = CRUDFood(Food)
