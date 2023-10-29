import os
from datetime import datetime
from typing import Any

from app import crud
from app.db.session import AsyncSession, SessionLocal, engine
from app.models import Base, Canteen, Food, Weigh


class Init:
    def __init__(self) -> None:
        ...

    async def add_batch(self, db: AsyncSession, batch: list[Any]):
        db.add_all(batch)
        await db.commit()
        for db_obj in batch:
            await db.refresh(db_obj)
        return batch


async def init_db():
    """Initialize the database and add a default superuser."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    if os.getenv("CREATE_ONLY") == "true":
        return

    print("===Init data===")

    async with SessionLocal() as db:
        canteens = [
            Canteen(name="新桃", aliases=["桃北"], desc="新宇"),
            Canteen(name="旧桃", aliases=["桃南"], desc=""),
            Canteen(name="梅园", aliases=[], desc="华工"),
        ]
        await crud.canteen.adds(db, canteens)
        food = await crud.food.add(db, Food(name="测试食物", aliases=["AAA", "BBB"], price=10, desc="descsfdf"))
        await crud.weigh.add(db, Weigh(canteen=canteens[1], food=food, weight=100, record_date=datetime.now().date()))
