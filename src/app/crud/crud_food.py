from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.food import Food
from app.models.weigh import Weigh


class CRUDFood(CRUDBase[Food, BaseModel, BaseModel]):
    async def get_with_weight(self, db: AsyncSession):
        stmt = select(
            Food, select(func.avg(Weigh.weight)).where(Food.id == Weigh.food_id).as_scalar().label("avg_weight")
        )
        return list((await db.execute(stmt)).all())


food = CRUDFood(Food)
