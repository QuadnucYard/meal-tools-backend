import asyncio
from datetime import datetime
import sys

import pandas as pd

from app import crud
from app.db.session import AsyncSession, SessionLocal, engine
from app.db.utils import no_echo
from app.models import Base, Canteen, Food, Weigh


class Init:
    def __init__(self) -> None:
        self.foods = list[Food]()
        self.weighs = list[Weigh]()
        self.food_dict = dict[str, Food]()

    async def init_canteens(self, db: AsyncSession):
        self.canteens = [
            Canteen(name="新桃", aliases=["桃北"], desc="新宇"),
            Canteen(name="旧桃", aliases=["桃南"], desc=""),
            Canteen(name="梅园", aliases=[], desc="华工"),
        ]
        await crud.canteen.adds(db, self.canteens)
        self.canteen_dict = {c.name: c for c in self.canteens}

    async def init_all(self, db: AsyncSession, file: str):
        df = pd.read_excel(file, header=None).dropna(axis=0, how="all")
        df[[0, 3]] = df[[0, 3]].ffill(axis=0)
        df.dropna(axis=0, how="any", inplace=True)

        await self.init_canteens(db)

        for row in df.itertuples(False):
            if row[1] not in self.food_dict:
                food = Food(name=row[1], aliases=[], price=0, desc="")
                await crud.food.add(db, food)
                self.food_dict[food.name] = food
            self.weighs.append(
                Weigh(
                    canteen=self.canteen_dict[row[3]],
                    food=self.food_dict[row[1]],
                    weight=int(row[2]),
                    record_date=row[0],
                )
            )
        await crud.weigh.adds(db, self.weighs)


async def init_db(file: str):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with SessionLocal() as db:
        with no_echo(engine):
            ini = Init()
            await ini.init_all(db, file)


if __name__ == "__main__":
    asyncio.run(init_db(sys.argv[1]))
