from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.food import Food
from app.models.weigh import Weigh


class CRUDWeigh(CRUDBase[Weigh, BaseModel, BaseModel]):
    async def get_recent_foods(self, db: AsyncSession, limit: int):
        # 按照最晚一次登记顺序
        stmt = (
            select(Food.id)
            .order_by(select(func.max(Weigh.create_time)).where(Weigh.food_id == Food.id).as_scalar().desc())
            .limit(limit)
        )
        return (await db.execute(stmt)).scalars()

    async def get_food_rc(self, db: AsyncSession, food_id: int):
        stmt = select(func.count()).select_from(Weigh).where(Weigh.food_id == food_id)
        return (await db.execute(stmt)).scalar_one()


weigh = CRUDWeigh(Weigh)
